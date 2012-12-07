#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier en charge de l'affichage et de l'animation du système
"""

import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
#from corps import *
#from systeme import *
import numpy

#création de la figure qui sera affichée - à passer dans le main
fig = pyplot.figure()
ax = fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim=[-2.1,1.1], ylim=[-2.1,1.1])

#affichage d'un système vide qui sera modifié au cours de l'animation. En fait on crée ici notre univers visuel - à passer dans le main
univers, = ax.plot([], [], 'bo', ms=5)
energie_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes)

#le bloc suivant est un outil de déboggage de ce fichier
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

def initialisation():
	"""
	Donne les prarmètres de départ de l'animation.
	"""
	univers.set_data([], [])
	energie_texte.set_text('') #on initialise le système puis l'affichage l'énergie avec rien. Nécessaire à l'animation avec FuncAnimation
	
	return univers, energie_texte #on retourne les objets qui seront modifiés par l'animation à chaque frame

def animer(i):
	"""
	Génère l'animation de la frame i en actualisant les positions de la frame i-1.
	"""
#	global systeme, dt #on récupère le système et la durée entre deux frames. Essayons sans les global d'abord
	systeme.iteration(dt) #on actualise les positions du système

	univers.set_data(*systeme.positions()) #on actualise les positions dans les données à afficher. L'étoile spécifie à la méthode qu'on utilise un argument qui a un nom. Sinon elle crie
	energie_texte.set_text('energie = %.3f J' % systeme.energie()) #on affiche la nouvelle énergie. J'ai pensé que 3 chiffres significatifs suffisaient mais si tu veux en rajouter, fais-toi plaisir

	return univers, energie_texte

#on fixe ensuite l'intervalle en fonction de dt et de la durée séparant deux frames. Du gros repompé de GitHub, mais on va voir comment ça se comporte - à passer dans le main
import time
t0 = time.time()
animer(0)
t1 = time.time()
intervalle = 1000 * dt - (t1 - t0) #ai pas compris ca. À examiner de plus près. On peut peut-être balancer un intervalle arbitraire pour simplifier


if __name__=="__main__": #partie à utiliser pour les tests

	anim = animation.FuncAnimation (fig, animer, frames=300, interval=intervalle, blit=True, init_func=initialisation)

	pyplot.show()
