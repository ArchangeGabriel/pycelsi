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
from animation2 import *
from matplotlib.animation import FuncAnimation
from time import time

periode_affichage = 0.05 # Inverse du nombre d'images par seconde

# Obtention des paramètres de l'animation et du système - A déplacer dans la lecture de l'entrée standard
temps_relatif = 105192
calc_per_frame = 100
fpxmax = True
wait = 0.0
temps_sys = 86400*365.25*0.12

# On calcule le pas de temps en fonction du nombre d'images par seconde, du coefficient de dilation du temps et du nombre de calculs par image voulu
dt = periode_affichage * temps_relatif / calc_per_frame

# On itère le système d'un coup
sys = []
n = int(temps_sys / temps_relatif / periode_affichage)
print n * calc_per_frame

t0 = time()

# Version lente. Conserve bien l'énergie, d'autant plus que le nombre de calcul par image est élevé. Pour un calcul par image, même perte que la méthode propre, ce qui est logique étant donné que cela revient strictement au même.
#for i in range(n) :
#    for j in range(calc_per_frame):
#        systeme.iteration(dt, 1)
#    sys.append(systeme.positions()+[systeme.E_T+systeme.E_V])

for i in range(n) :
    systeme.iteration2(dt, calc_per_frame)
    sys.append(systeme.positions()+[systeme.E_T+systeme.E_V])

# Version propre, beaucoup plus rapide mais conserve mal l'énergie. D'ailleurs, il semblerait que la perte d'énergie ne dépende pas trop du nombre de calculs par image.
#for i in range(n) :
#    systeme.iteration(dt, calc_per_frame)
#    sys.append(systeme.positions()+[systeme.E_T+systeme.E_V])

t1 = time()

print t1-t0

T = time()

# Animation de l'affichage
if fpxmax :
    intervalle = 1 # Version qui ne dépend que du temps de calcul, trop rapide donc, mais peut être ralentie avec wait
else :
    intervalle = periode_affichage * 1000 # Cette version est la "bonne", mais ne fonctionne pas car l'animation ne respecte pas interval...

anim = FuncAnimation (fig, animer, range(n), fargs=(sys, T, periode_affichage, temps_relatif, wait), interval=intervalle, blit=True, init_func=initialisation)

pyplot.show()
