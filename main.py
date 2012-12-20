#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corps import *
from systeme import *
import numpy
UA = 1.49597871e11 #une UA en m




#---------------------------création du système--------------------------- version d'essai


#systeme = Systeme([['soleil',0,0,0,0,1.392684e9/2,1.9891e30],['terre',1*UA,0,0,2*numpy.pi*1*UA/365.25696/24/3600,6.3710e6,5.9736e24]])
systeme= Systeme ([['soleil',0,0,0,0,0.1,6.573491451e10],['terre',0,-1,2*numpy.pi/3,0,0.1,1e1],['terre',0,1,-2*numpy.pi/3,0,0.1,1e1]])




#-------------------------affichage et animations-------------------------


import matplotlib.pyplot as pyplot
import matplotlib.animation
from time import time

from animation import *




#--------réglage de la vitesse d'affichage--------------------------------


#on fixe l'intervalle en fonction de la période d'affichage souhaitée et de la durée d'affichage d'une frame, histoire d'en être indépendant
dt = periode_affichage*temps_relat/calc_par_frame #on fixe la période de calcul

t0 = time()
animer(0, calc_par_frame, systeme, dt)
t1 = time()

assert periode_affichage - (t1 - t0) > 0, "période d'affichage demandée %f s trop faible par rapport au temps d'affichage %f s" % (periode_affichage , t1-t0) # on ne pourra pas réduire la période de refresh en-dessous du temps nécessaire à l'affichage

periode_affichage = periode_affichage - (t1 - t0) #on adapte la période d'affichage pour coller au temps spécifié initialement




#--------animation du système---------------------------------------------


anim = matplotlib.animation.FuncAnimation (fig, animer, fargs=(calc_par_frame, systeme, dt), frames=300, interval=periode_affichage*1000, blit=True, init_func=initialisation)
pyplot.show()
