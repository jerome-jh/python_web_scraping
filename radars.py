#!/usr/bin/python3

import os
import re
import sys
import copy
import requests
from bs4 import BeautifulSoup
import dict_object

cache_dir = 'cache'
all_pictos = set()

class Radar(dict_object.DictObject):
    pass

def get_scripts_no_src(soup):
    r = list()
    scripts = soup.find_all('script')
    for s in scripts:
        try:
            s['src']
        except KeyError:
            r.append(s)
    return r

def download(path):
    filename = os.path.join(cache_dir, path + '.html')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.isfile(filename):
        print('Read cached', filename);
        f = open(filename, 'rb')
        html = f.read()
        f.close()
        return html
    else:
        url = base_url
        if (len(path)):
            url = base_url + path + '/'
        print('Downloading', url);
        html = requests.get(url)
        html.raise_for_status()
        f = open(filename, 'wb+')
        f.write(html.content)
        f.close()
        return html.content

def parse_picto(radar, url):
    ## Cache regex
    global picto_reg, type_reg
    try:
        picto_reg
    except NameError:
        ## Split: path, name., extension
        picto_reg = re.compile(r'(.*/)*(.+\.)+(\w{3,4})')
    m = picto_reg.match(url)
    #print(m.groups())
    if m:
        name = m.group(2)
    else:
        print(url, 'not recognized')
    try:
        type_reg
    except NameError:
        type_reg = re.compile(r'picto-vitesse-(?P<speed>\d*)\.|picto-radar-(?P<fixed>\w*gen\w*)\.|picto-radar-(?P<redlight>\w*feu\w*)\.|picto-radar-(?P<fake>\w*(pedago|leurre)\w*)\.|picto-radar-(?P<gate>[-\w]*niveau[-\w]*)\.|picto-radar-(?P<section>\w*troncon\w*)\.')
    m = type_reg.match(name)
    radar.type = m.lastgroup
    if radar.type == 'speed':
        if len(m.group(1)):
            radar.speed = int(m.group(1))
    ## set speed anyway for all types
    radar.speed = 0
    #print(radar)
                
def parse_departement(departement):
    html = download('emplacements/' + departement)
    soup = BeautifulSoup(html, "lxml")
    scripts = get_scripts_no_src(soup)

    ## Find images
    images = list()
    reg = re.compile(r'var\s+image\S+\s*=\s*\{.*?\}\s*;', re.DOTALL)
    for s in scripts:
        m = reg.findall(s.text)
        if m:
            images.extend(m)

    print('Images', len(images))
    #print(images)

    ## Define images as variables in order to parse radars
    image_urls = set()
    reg = re.compile(r'var\s+(image\S+)\s*=\s*\{.*?url\s*:\s*\'(.*?)\'.*?\}\s*;', re.DOTALL)
    for i in range(len(images)):
        m = reg.match(images[i])
        if m:
            name, url = m.group(1, 2)
            locals()[name] = url
            image_urls.add(url)
        else:
            print("Failed to parse image")
            quit()
   
    ## Find radars
    radars = list()
    reg = re.compile(r'var\s+radars\s*=\s*(\[.*?\])\s*;', re.DOTALL)
    for s in scripts:
        m = reg.search(s.text)
        if m:
            rads = eval(m.group(1))
            for r in rads:
                rad = Radar(['name', 'lat', 'lon', 'picto', 'html'], r)
                radars.append(rad)
    
    print('Radars', len(radars))
    #print(radars[0])

    #for r in radars:
    #    print(r[0])

    for r in radars:
        s = BeautifulSoup(r.html, "lxml")
        imgs = s.find_all('img')
        #print(imgs)
        for i in imgs:
            #print(i['src'])
            all_pictos.add(i['src'])
            parse_picto(r, i['src'])
        #all_pictos.add(imgs[1]['src'])
    #print(all_pictos)
    
    return image_urls, radars

def get_departements():
    html = download('emplacements')
    soup = BeautifulSoup(html, "lxml")
    #ldiv = soup.find_all('div')
    #reg = re.compile(r'liste.*?département', re.IGNORECASE)
    #for d in ldiv:
    #    m = reg.match(d.text)
    #    if m:
    #        print(d)
    #        div = d
    #        break
    departements = list()
    la = soup.find_all('a')
    reg = re.compile(r'/emplacements/(.*?)/')
    for a in la:
        m = reg.match(a['href'])
        if m:
            departements.append(m.group(1))
    return departements

def write_kml(radars):
    ## TODO: not loaded by myspeed
    ## Add image
    f = open('radars.kml', 'wt')
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("   <name>radars.kml</name>\n")
    for r in radars:
        f.write("   <Placemark>\n")
        f.write("       <name>" + r.name + "</name>\n")
        #f.write("       <description>" + r[4] + "</description>\n")
        f.write("       <Point>\n")
        f.write("           <coordinates>" + str(r.lon) + "," + str(r.lat) + "</coordinates>\n")
        f.write("       </Point>\n")
        f.write("   </Placemark>\n")
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()

def write_csv(radars):
    ## TODO: write speed
    type_dict = {
        'fixed': 1,
        'redlight': 3,
        'section': 4,
        'gate': 6,
        'fake': 0
    }
    f = open('radars.csv', 'wt')
    f.write("X,Y,TYPE,SPEED,DIRTYPE,DIRECTION\n")
    for r in radars:
        f.write(str(r.lon) + ',' + str(r.lat) + ',' + type_dict[r.type] + ',' + str(r.speed) + ',0,0\n')
    f.close()

if __name__ == '__main__':
    base_url = sys.argv[1]
    if base_url[-1] != '/':
        base_url += '/'

    ## fetch departement list
    departements = get_departements()
    print('Departements', len(departements))

    images = set()
    radars = list()
    for d in departements:
    #for d in departements[37:38]:
        i, r = parse_departement(d)
        images.update(i)
        radars.extend(r)

    print('Total images', len(images))
    print('Total radars', len(radars))

    print(all_pictos)
    write_csv(radars)
    write_kml(radars)

    #for g in gps:
    #    directory = projet + '_' + g.upper()
    #    os.mkdir(directory)
    #    os.chdir(directory)
    #    for d in departements:
    #        download_departement(projet, d, g)
    #    os.chdir('..')
    
