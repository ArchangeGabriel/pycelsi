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
ax = fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim=[-1.1*UA,1.1*UA], ylim=[-1.1*UA,1.1*UA])


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

	t0 = time()	

	while time() - t0 < periode_affichage / 1000 :
		systeme.iteration(dt)

	univers.set_data(*systeme.positions()) #l'étoile spécifie à la méthode qu'on utilise un argument qui a un nom. Sinon elle crie
	energie_texte.set_text('energie = %.3e J' % (systeme.E_T+systeme.E_V)) #j'ai pensé que 3 décimales suffisaient

	return univers, energie_texte


#on peut fixer l'intervalle en fonction de dt et de la durée séparant deux frames. Du gros repompé de GitHub, mais on va voir comment ça se comporte
#from time import time
#t0 = time()
#animer(0)
#t1 = time()
#intervalle = 1000 * dt - (t1 - t0) #ai pas compris ca. À examiner de plus près. En attendant j'ai balancé un intervalle arbitraire pour simplifier


#animation et affichage à proprement parler
anim = matplotlib.animation.FuncAnimation (fig, animer, frames=300, interval=periode_affichage, blit=True, init_func=initialisation)
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
