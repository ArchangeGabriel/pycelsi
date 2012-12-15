#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corps import *
from systeme import *
import numpy
UA = 1.49597871e11 #une UA en m


#---------------------------création du système--------------------------- version d'essai

#systeme = Systeme([['soleil',0,0,0,0,1.392684e9/2,1.9891e30],['terre',1*UA,0,0,2*numpy.pi*1*UA/365.25696/24/3600,6.3710e6,5.9736e24]])
systeme= Systeme ([['soleil',0,0,0,0,0.1,6.573491451e10],['terre',0,-1,2*numpy.pi/3,0,0.1,1e1],['terre',0,1,-2*numpy.pi/3,0,0.1,1e1]])


#--------------------réglage de la vitesse d'affichage--------------------

temps_relat = 0.1 #coefficient d'écoulement du temps par rapport au temps réel
periode_affichage = 0.025 #en s, période d'affichage d'une nouvelle image
calc_par_frame = 5 #nombre de calculs par image


#-------------------------affichage et animations-------------------------

from animation import *
