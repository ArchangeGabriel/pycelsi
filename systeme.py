#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier de classe du système de corps
"""

from corps import *

from scipy.integrate import odeint

class Systeme (object) :
    """Classe de représentation d'un système de corps"""

    def __init__ (self, l, G = 6.67384e-11) :
        """Instanciation d'un système à partir d'une liste de corps et de G"""

        self.G = G

        self.corps = []

        self.n = 0

        for corps in l :
            self.corps += [Corps(corps[0], corps[1], corps[2], corps[3], corps[4], corps[5], corps[6])]
            self.n += 1

    def __str__ (self) :
        """Surcharge de l'opérateur str() pour la classe Système"""

    def vect_deriv (self, z, t) :
        """Vecteur des relations dérivées sur x, vx, y, vy"""

        for i in range(0, self.n) :
            z[4*i] = z[4*i+1]
            z[4*i+1] = 0
            z[4*i+2] = z[4*i+3]
            z[4*i+3] = 0

        for i in range(0, self.n - 1) :
            for j in range (i + 1, self.n) :
                f = self.corps[i].force(self.corps[j], self.G)
                z[4*i+1] += f[0] / self.corps[i].m
                z[4*i+3] += f[1] / self.corps[i].m
                z[4*j+1] -= f[0] / self.corps[j].m
                z[4*j+3] -= f[1] / self.corps[j].m

        return z

    def iteration (self, dt) :
        """Iteration de l'état du système"""

        z = []

        for corps in self.corps :
            z += [corps.x, corps.vx, corps.y, corps.vy]

        dz = odeint(self.vect_deriv, z, [0, dt])

        for i in range(0, self.n) :
            self.corps[i].x += dz[1][4*i]
            self.corps[i].vx += dz[1][4*i+1]
            self.corps[i].y += dz[1][4*i+2]
            self.corps[i].vy += dz[1][4*i+3]

    def positions (self) :
        """Renvoie la liste des positions des corps du système"""

        z = [[],[]]

        for corps in self.corps :
            z[0] += [corps.x]
            z[1] += [corps.y]

        return z

    def energie (self) :
	"""Renvoie l'énergie du système. Doit être conservée si tout se passe bien"""

	return 1 #oui c'est provisoire
