#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier en charge de l'affichage et de l'animation du système
"""

import matplotlib.pyplot as pyplot
from time import time

# Création de la figure qui sera affichée
fig = pyplot.figure()
ax = fig.add_subplot(111, autoscale_on = False, xlim=[-1.5e11,1.5e11], ylim=[-1.5e11,1.5e11])

# Création d'un système vide qui sera modifié au cours de l'animation. En fait on crée ici notre "univers visuel"
univers, = ax.plot([], [], 'bo', markersize=5)
energie_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)
temps_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def initialisation():
    """
    Initialise une première frame vide pour donner à FuncAnimation les objets à modifier à chaque frame.
    """

    univers.set_data([], [])
    energie_texte.set_text('\n\n')
    temps_texte.set_text('\n\n')
    
    return univers, energie_texte, temps_texte

def animer(i, systeme, calc_per_frame, periode_affichage, temps_relat, dt):
    """
    Génère l'animation de la frame i en actualisant les positions et l'énergie de la frame i-1 et en envoyant le résultat dans l'"univers visuel"
    """

    t0 = time()

    for calc in range (0,calc_per_frame) :
        systeme.iteration(dt)

    duree_reel = periode_affichage * i
    duree_sys = duree_reel * temps_relat

    t1 = time()

    univers.set_data(*systeme.positions()) # * spécifie à la méthode qu'on utilise un argument qui "a un nom"
    energie_texte.set_text("Energie = %.4e J\n\n" % (systeme.E_T+systeme.E_V)) # 5 Chiffres significatifs
    temps_texte.set_text("Temps : %.3f s  Effectif : %.2f s" % (duree_sys, duree_reel))

    # Pour ralentir l'exécution mais c'est crade, et ça dépend de la machine
    #while t1 - t0 < 0.041 :
    #    t1 = time()

    # Ecart entre le temps réellement écoulé et duree_reel
    print t1 - systeme.time - duree_reel

    return univers, energie_texte, temps_texte
