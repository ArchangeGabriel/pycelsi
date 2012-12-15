#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier en charge de l'affichage et de l'animation du système
"""

import matplotlib.pyplot as pyplot
import matplotlib.animation
from systeme import *
from main import *
from time import time


#création de la figure qui sera affichée
fig = pyplot.figure()
ax = fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim=[-1.5,1.5], ylim=[-1.5,1.5])


#création d'un système vide qui sera modifié au cours de l'animation. En fait on crée ici notre "univers visuel"
univers, = ax.plot([], [], 'bo', markersize=5)
energie_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def initialisation():
    """
    Initialise une première frame vide pour donner à FuncAnimation les objets à modifier à chaque frame.
    """
    univers.set_data([], [])
    energie_texte.set_text('')
    
    return univers, energie_texte


def animer(i):
    """
    Génère l'animation de la frame i en actualisant les positions et l'énergie de la frame i-1 et en envoyant le résultat dans l'"univers visuel"
    """

    for calc in range (0,calc_par_frame) :
        systeme.iteration(dt)

#    print systeme.positions()

    univers.set_data(*systeme.positions()) #l'étoile spécifie à la méthode qu'on utilise un argument qui a un nom. Sinon elle crie
    energie_texte.set_text('energie = %.3e J' % (systeme.E_T+systeme.E_V)) #j'ai pensé que 3 décimales suffisaient

    return univers, energie_texte


#on peut fixer l'intervalle en fonction de la période d'affichage souhaitée et de la durée d'affichage d'une frame, histoire d'en être indépendant
dt = periode_affichage*temps_relat/calc_par_frame #on fixe la période de calcul
from time import time
t0 = time()
animer(0)
t1 = time()
assert periode_affichage - (t1 - t0) > 0, "période d'affichage demandée %f s trop faible par rapport au temps d'affichage %f s" % (periode_affichage , t1-t0) # on ne pourra pas réduire la période de refresh en-dessous du temps nécessaire à l'affichage
periode_affichage = periode_affichage - (t1 - t0) #on adapte la période d'affichage pour coller au temps spécifié initialement


#animation et affichage à proprement parler
anim = matplotlib.animation.FuncAnimation (fig, animer, frames=300, interval=periode_affichage*1000, blit=True, init_func=initialisation)
pyplot.show()


if __name__=="__main__": #partie codée avec les pieds à utiliser pour les tests

    import numpy

    class corps(object):
        def energie(self):
            return 1
        def iteration(self, dt):
            global a
            a += 0.01
            self.x = numpy.cos(a)
            self.y = numpy.sin(a)
        def positions(self):
            return [[self.x,0.5*self.x-1,0.5*self.x**5-0.5],[0.5*self.y,self.y-1,0.5*self.y**5-0.5]]

    dt=1/30    
    systeme=corps()
    systeme.x=0
    systeme.y=0
    a = 0.
