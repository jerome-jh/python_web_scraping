#!/usr/bin/python3

## Remote script never returns more than 500 results
## Some 'regions' have more than 500 POI's
## That is why we download by 'departement'

import os
import sys
import copy
import requests
from bs4 import BeautifulSoup

projet = 'France'
gps = ['gpx', 'csv']

start_params = {'Projet':''}

genere_url = 'http://www.t4t35.fr/Megalithes/GenereGPX.aspx'
genere_params = {
    'GPS': 'GPX', #'CSV'
    'Projet': '',
    'Nom': '',
    'Symbole': '',
    'CodeRegroupe': '',
    'Commune': '',
    'Departement': '',
    'Region': '',
    'Coordonnees': '',
    'Visite': 'Tous',
    'DateVisiteMin': '',
    'DateVisiteMax': '',
    'Type': '',
    'Date': '',
    'Propriete': '',
    'Valeur': '',
    'MotClef': '',
    'Nombre': '',
    'Tri': '[IDSite]',
    'Action': 'Télécharger',
}

def get_select(html, name):
    sel = soup.find_all('select')
    for s in sel:
        if s['name'] == name:
            return s

def get_option_values(html):
    values = list()
    opt = html.find_all('option')
    for o in opt:
        if len(o['value']):
            values.append(o['value'])
    return values

def get_regions(html):
    sel = get_select(html, 'Region')
    return get_option_values(sel)

def get_departements(html):
    sel = get_select(html, 'Departement')
    return get_option_values(sel)

def download_departement(projet, departement, gps='gpx'):
    print('Downloading', projet, departement);
    params = copy.deepcopy(genere_params)
    params['Projet'] = projet
    params['Departement'] = departement
    params['GPS'] = gps.upper()
    html = requests.get(genere_url, params = params)
    html.raise_for_status()
    f = open(departement + '.' + gps, 'wb+')
    f.write(html.content)
    f.close()

if __name__ == '__main__':
    if sys.argv[1].endswith('.html'):
        url = sys.argv[1]
        print('Reading', url)
        f = open(sys.argv[1], 'rb')
        html = f.read()
        f.close()
    else:
        url = sys.argv[1] + '/Megalithes/AffichePresentation.aspx'
        params = copy.deepcopy(start_params)
        print('Downloading', url)
        params['Projet'] = projet
        html = requests.get(url, params = params)
        print(html.url)
        html.raise_for_status()
        f = open('cache.html', 'wb+')
        f.write(html.content)
        f.close()
        html = html.content

soup = BeautifulSoup(html, "lxml")
regions = get_regions(soup)
departements = get_departements(soup)

for g in gps:
    directory = projet + '_' + g.upper()
    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)
    for d in departements:
        download_departement(projet, d, g)
    os.chdir('..')

