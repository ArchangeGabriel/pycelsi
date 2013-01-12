#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "Time-stamp: <2013-01-13 00:30:49 bpagani>"
__author__ = "Bruno Pagani <bruno.n.pagani@gmail.com>, \
              Denis Ibanez <denis.ibanez@ens-lyon.fr>"

"""
Fichier en charge de l'affichage et de l'animation du système
"""

import matplotlib.pyplot as pyplot
from matplotlib.animation import FuncAnimation
from time import time, sleep

# Création de la figure qui sera affichée
fig = pyplot.figure()
ax = fig.add_subplot(111)

# Création d'un système vide qui sera modifié au cours de l'animation. En 
# fait, on crée ici notre "univers visuel".
univers, = ax.plot([], [], 'bo', markersize=5)
energie_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)
temps_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def set_size (size) :
    """
    Ajustement de la taille du graphe.
    """
    ax.set_xlim(-size,size)
    ax.set_ylim(-size,size)


def initialisation () :
    """
    Initialise une première frame vide pour donner à FuncAnimation les objets à 
    modifier à chaque frame.
    """

    univers.set_data([], [])
    energie_texte.set_text('\n\n')
    temps_texte.set_text('\n\n')
    
    return univers, energie_texte, temps_texte


def animer (i, systeme, periode_affichage, temps_relatif, T, 
            wait=0, calc_per_frame=0, dt=0, method=0) :
    """
    Génère l'image i à partir de l'itération du système.
    """

    t0 = time()

    if type(systeme) == list :
        lsys = systeme[i]
    else :
        lsys = systeme.itern(dt, calc_per_frame, 1, method)[0]

    duree_reel = periode_affichage * i
    duree_sys = duree_reel * temps_relatif

    univers.set_data(lsys[:-1])
    energie_texte.set_text("Energie = %.4e J\n\n" % (lsys[-1]))
    temps_texte.set_text("Temps : %.3f s  Effectif : %.2f s"
                         % (duree_sys, duree_reel))

    t1 = time()

    # Pour ralentir l'exécution, mais ça dépend de la machine
    if wait :
        t = wait-t1+t0
        if t > 0 :
            sleep(t)

    # Ecart entre le temps réellement écoulé et duree_reel
    print t1 - T - duree_reel

    return univers, energie_texte, temps_texte


def generation_affichage (systeme, periode_affichage, temps_relatif, wait, 
                          calc_per_frame, method, temps_sys, size) :
    """
    Fonction qui génère le contenu à animer.
    """

    set_size(size)

    # On calcule le pas de temps
    dt = periode_affichage * temps_relatif / calc_per_frame

    # Animation de l'affichage
    if wait :
        lapse = 1 # Affichage limité par la vitesse de calcul
    else :
        lapse = periode_affichage * 1000 # Affichage réglé aux FPS demandé
        # Cette version est la "bonne", mais ne fonctionne pas car l'animation 
        # ne respecte pas interval...

    # Si temps_sys est non nul, alors on fait évoluer le système autant de temps
    if temps_sys :

        # On itère le système d'un coup, n = nombre d'images à afficher/calculer
        n = int(temps_sys / temps_relatif / periode_affichage)
        print n * calc_per_frame

        t0 = time()
        sys = systeme.itern(dt, calc_per_frame, n, method)
        t1 = time()

        # On affiche le temps d'exécution de l'itération du système
        print t1-t0

        return FuncAnimation(fig, animer, range(n),
                             fargs=(sys, periode_affichage, temps_relatif, 
                                    time(), wait), 
                             interval=lapse, blit=True, init_func=initialisation)

    else :

        # On effectue le premier tour d'animation pour tester si le temps de 
        # calcul n'est pas trop long dans le cas où c'est lui qui limite.
        if not wait :
            t0 = time()
            animer(0, systeme, periode_affichage, temps_relatif, 
                   time(), wait, calc_per_frame, dt, method)
            t1 = time()

            assert periode_affichage > (t1 - t0), ("Période d'affichage demandée\
                %f s trop faible par rapport au temps d'affichage effectif %f s" 
                % (periode_affichage , t1-t0))

            # On réinitialise le système
            systeme.reset()

        return FuncAnimation(fig, animer, 
                             fargs=(systeme, periode_affichage, temps_relatif, 
                                    time(), wait, calc_per_frame, dt, method), 
                             interval=lapse, blit=True, init_func=initialisation)


def animation (systeme, periode_affichage, temps_relatif, wait, 
               calc_per_frame, method, temps_sys, size) :
    """
    Fonction affichant l'animation.
    """

    anim = generation_affichage(systeme, periode_affichage, temps_relatif, wait, 
                                calc_per_frame, method, temps_sys, size)

    pyplot.show()
