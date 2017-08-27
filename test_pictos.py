#!/usr/bin/python3

import radars

known_pictos = [
    '/images/pictos/picto-vitesse-60.jpg',
    '/images/pictos/picto-vitesse-80.jpg',
    '/images/pictos/picto-vitesse-130.jpg',
    '/images/pictos/picto-vitesse-30.jpg',
    '/images/pictos/picto-vitesse-110.jpg',
    '/images/pictos/picto-vitesse-70.jpg',
    '/images/pictos/picto-vitesse-50.jpg',
    '/images/pictos/picto-vitesse-.jpg',
    '/images/pictos/picto-vitesse-90.jpg',
    '/images/pictos/picto-vitesse-45.jpg',
    '/images/pictos/picto-radar-pedagogique.jpg',
    '/images/pictos/picto-radar-leurre.jpg',
    '/images/pictos/picto-radar-gen30.jpg',
    '/images/pictos/picto-radar-gen4.jpg',
    '/images/pictos/picto-radar-gen2.jpg',
    '/images/pictos/picto-radar-gen1.jpg',
    '/images/pictos/picto-radar-gen3.jpg',
    '/images/pictos/picto-radar-passage-niveaux.jpg',
    '/images/pictos/picto-radar-feux.jpg',
    '/images/pictos/picto-radar-troncon.jpg',
]

if __name__ == '__main__':
    for p in known_pictos:
        radars.parse_picto(radars.Radar(), p)
