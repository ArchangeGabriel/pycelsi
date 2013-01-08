#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier en charge de l'affichage et de l'animation du système
"""

import matplotlib.pyplot as pyplot

periode_affichage = 0.05 # Inverse du nombre d'images par seconde

# Obtention des paramètres de l'animation et du système - A déplacer dans la lecture du fichier de conf
temps_relat = 105192
calc_par_frame = 100

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


def animer(i, systeme, dt):
    """
    Génère l'animation de la frame i en actualisant les positions et l'énergie de la frame i-1 et en envoyant le résultat dans l'"univers visuel"
    """

    for calc in range (0,calc_par_frame) :
        systeme.iteration(dt)
        systeme.duree_sys += dt

    systeme.duree_reel += periode_affichage

    univers.set_data(*systeme.positions()) # * spécifie à la méthode qu'on utilise un argument qui "a un nom"
    energie_texte.set_text('Énergie = %.4e J\n\n' % (systeme.E_T+systeme.E_V)) # 5 Chiffres significatifs
    temps_texte.set_text('Temps : %.3f s  Effectif : %.2f s' % (systeme.duree_sys, systeme.duree_reel))

    return univers, energie_texte, temps_texte
