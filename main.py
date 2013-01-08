#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier principal du projet, qui utilise les autres pour réaliser la simulation proprement dite
"""

# On importe le fichier systeme.py qui contient la classe Systeme et les méthodes qui s'y appliquent
from systeme import *

# Création du système - Version temporaire pour les tests, prochainement lecture depuis un fichier
systeme = Systeme([['soleil','jaune',0,0,0,0,1.392684e9/2,1.9891e30],['terre','bleu',1.495978875e11,0,0,29783,6.3710e6,5.9736e24]])



# Affichage et animations
from animation import *
from matplotlib.animation import FuncAnimation
from time import time


# On calcule le pas de temps en fonction du nombre d'images par seconde, du coefficient de dilation du temps et du nombre de calculs par image voulus
dt = periode_affichage * temps_relat / calc_par_frame

# On effectue le premier tour d'animation pour tester si le temps de calcul n'est pas trop long
t0 = time()
animer(0, systeme, dt)
t1 = time()

assert periode_affichage > (t1 - t0), "Période d'affichage demandée %f s trop faible par rapport au temps d'affichage effectif %f s" % (periode_affichage , t1-t0)


# Animation de l'affichage
anim = FuncAnimation (fig, animer, fargs=(systeme, dt), interval=periode_affichage*1000, blit=True, init_func=initialisation)
pyplot.show()
