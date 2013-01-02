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

        self.E_T = 0
        self.E_V = 0

        self.duree_sys = 0
        self.duree_reel = 0

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

        self.E_T = 0
        self.E_V = 0

        for corps in self.corps :
            self.E_T += corps.energie_ki()

        for i in range(0, self.n - 1) :
            for j in range (i + 1, self.n) :
                Vf = self.corps[i].potentiel_force(self.corps[j], self.G)
                self.E_V -= Vf[0]
                f = Vf[1]
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
            self.corps[i].x += dz[1][4*i]*dt
            self.corps[i].vx += dz[1][4*i+1]*dt
            self.corps[i].y += dz[1][4*i+2]*dt
            self.corps[i].vy += dz[1][4*i+3]*dt

    def positions (self) :
        """Renvoie la liste des positions des corps du système"""

        z = [[],[]]

        for corps in self.corps :
            z[0] += [corps.x]
            z[1] += [corps.y]

        return z
