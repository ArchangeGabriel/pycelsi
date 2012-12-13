#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corps import *
from systeme import *
import numpy
UA = 1.49597871e11 #une UA en m


#---------------------------création du système--------------------------- version d'essai

systeme = Systeme([['soleil',0,0,0,0,1.392684e9/2,1.9891e30],['terre',1*UA,0,0,2*numpy.pi*1*UA/365.25696/24/3600,6.3710e6,5.9736e24]])

#--------------------réglage de la vitesse d'affichage--------------------

temps_relat = 365.25696*24*3600/10000 #ce qui devrait faire un tour en 5s dans ces essais
periode_affichage = 1000 #en ms
dt = temps_relat #en s Il semblerait qu'affecter ainsi dt perturbe le fonctionnement d'odeint. À travailler.


#-------------------------affichage et animations-------------------------

from animation import *
