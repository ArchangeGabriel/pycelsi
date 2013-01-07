#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier en charge de l'affichage et de l'animation du système
"""


import numpy
import matplotlib.pyplot as pyplot

periode_affichage = 0.05 # inverse du nombre d'images par seconde

#obtention des paramètres de l'animation et du système
parametres = numpy.genfromtxt('parametres.txt')
temps_relat = parametres[parametres.shape[0]-2]
calc_par_frame = int(parametres[parametres.shape[0]-1])


#création de la figure qui sera affichée
fig = pyplot.figure()
ax = fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim=[-1.5e11,1.5e11], ylim=[-1.5e11,1.5e11])


#création d'un système vide qui sera modifié au cours de l'animation. En fait on crée ici notre "univers visuel"
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

    univers.set_data(*systeme.positions()) #l'étoile spécifie à la méthode qu'on utilise un argument qui "a un nom"
    energie_texte.set_text('energie = %.3e J\n\n' % (systeme.E_T+systeme.E_V)) #j'ai pensé que 3 décimales suffisaient
    temps_texte.set_text('temps : %.3f s  effectif : %.2f s' % (systeme.duree_sys, systeme.duree_reel))

    return univers, energie_texte, temps_texte




#-plus bas ; partie obsolète codée avec les pieds utilisée pour les tests-


if __name__=="__main__":

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
