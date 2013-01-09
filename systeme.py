#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier de classe du système de corps
"""

# On importe le fichier corps.py qui contient la classe Corps et les méthodes qui s'y appliquent
from corps import *

# On importe la fonction odeint de scipy pour l'intégration numérique de dy/dt=f(y,t)
from scipy.integrate import odeint

# On définit la classe Systeme des système de corps
class Systeme (object) :
    """Classe de représentation d'un système de corps"""

    def __init__ (self, l, G = 6.67384e-11) :
        """Instanciation d'un système à partir d'une liste de corps et de G"""

        self.G = G # Constante de gravitation

        self.corps = []

        self.n = 0 # Nombre de corps dans le système

        self.E_T = 0 # Énergie cinétique totale du système, initialisée à 0
        self.E_V = 0 # Énergie potentielle totale du système, initialisée à 0

        for corps in l :
            self.corps += [Corps(corps[0], corps[1], corps[2], corps[3], corps[4], corps[5], corps[6], corps[7])]
            self.n += 1

        self.start = [l, G]

        self.time = 0

    def __str__ (self) :
        """Surcharge de l'opérateur str() pour la classe Système"""

        chaine = "Ce système est composé des corps :\n"

        for corps in self.corps :
            chaine += str(corps) + "\n"

        return chaine

    def reset (self) :
        """ Réinitialisation du système"""

        self.__init__(self.start[0], self.start[1])

    def vect_deriv (self, z, t) :
        """Vecteur des relations dérivées sur x, vx, y, vy"""

        dz = list()

        for i in range(0, self.n) :
            dz.append(z[4*i+1])
            dz.append(0)
            dz.append(z[4*i+3])
            dz.append(0)

        self.E_T = 0
        self.E_V = 0

        for corps in self.corps :
            self.E_T += corps.energie_ki()

        for i in range(0, self.n - 1) :
            for j in range (i + 1, self.n) :
                Vf = self.corps[i].potentiel_force(self.corps[j], self.G)
                self.E_V -= Vf[0]
                f = Vf[1]
                dz[4*i+1] += f[0] / self.corps[i].m
                dz[4*i+3] += f[1] / self.corps[i].m
                dz[4*j+1] -= f[0] / self.corps[j].m
                dz[4*j+3] -= f[1] / self.corps[j].m

        return dz

    def iteration (self, dt) :
        """Iteration de l'état du système"""

        z = []

        for corps in self.corps :
            z += [corps.x, corps.vx, corps.y, corps.vy]

        z = odeint(self.vect_deriv, z, [0, dt])[1]

        for i in range(0, self.n) :
            self.corps[i].x = z[4*i]
            self.corps[i].vx = z[4*i+1]
            self.corps[i].y = z[4*i+2]
            self.corps[i].vy = z[4*i+3]

    def positions (self) :
        """Renvoie la liste des positions des corps du système"""

        z = [[],[]]

        for corps in self.corps :
            z[0] += [corps.x]
            z[1] += [corps.y]

        return z
