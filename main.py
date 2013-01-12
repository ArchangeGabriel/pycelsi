#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier principal du projet, qui utilise les autres pour réaliser la simulation proprement dite
"""

# On importe le fichier systeme.py qui contient la classe Systeme et les méthodes qui s'y appliquent
from systeme import *

# Création du système - Version temporaire pour les tests, prochainement lecture depuis un fichier
systeme = Systeme([['Soleil','jaune',0,0,0,0,1.392684e9/2,1.9891e30],['Terre','bleu',1.495978875e11,0,0,29783,6.3710e6,5.9736e24]])



# Affichage et animations
from animation import *
from matplotlib.animation import FuncAnimation
from time import time

periode_affichage = 0.05 # Inverse du nombre d'images par seconde

# Obtention des paramètres de l'animation et du système - A déplacer dans la lecture de l'entrée standard
temps_relatif = 105192
calc_per_frame = 120
fpxmax = True
wait = 0.039

# On calcule le pas de temps en fonction du nombre d'images par seconde, du coefficient de dilation du temps et du nombre de calculs par image voulu
dt = periode_affichage * temps_relatif / calc_per_frame

# On effectue le premier tour d'animation pour tester si le temps de calcul n'est pas trop long
t0 = time()
animer(0, systeme, 0, calc_per_frame, periode_affichage, temps_relatif, dt, wait)
t1 = time()

assert periode_affichage > (t1 - t0), "Période d'affichage demandée %f s trop faible par rapport au temps d'affichage effectif %f s" % (periode_affichage , t1-t0)

# On réinitialise le système
systeme.reset()
T = time()

# Animation de l'affichage
if fpxmax :
    intervalle = 1 # Version qui ne dépend que du temps de calcul, trop rapide donc, mais peut être ralentie avec wait
else :
    intervalle = periode_affichage * 1000 # Cette version est la "bonne", mais ne fonctionne pas car l'animation ne respecte pas interval...

anim = FuncAnimation (fig, animer, fargs=(systeme, T, calc_per_frame, periode_affichage, temps_relatif, dt, wait), interval=intervalle, blit=True, init_func=initialisation)

pyplot.show()
