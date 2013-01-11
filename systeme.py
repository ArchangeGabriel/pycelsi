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

        # On stocke l'appel initial pour pouvoir réinitialiser le système en cas de besoin
        self.start = [l, G]

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
            dz.append(z[4*i+1]) # dx/dt = vx
            dz.append(0)
            dz.append(z[4*i+3]) # dy/dt = vy
            dz.append(0)

        self.E_T = 0
        self.E_V = 0

        for corps in self.corps :
            self.E_T += corps.energie_ki() # E_T = E_T(1) + ... + E_T(n)

        for i in range(0, self.n - 1) :
            for j in range (i + 1, self.n) :
                Vf = self.corps[i].potentiel_force(self.corps[j], self.G)
                self.E_V -= Vf[0] # E_V = E_V(1) + ... + E_V(n)
                f = Vf[1]
                dz[4*i+1] += f[0] / self.corps[i].m # d(vx1)/dt += Fx(2->1)
                dz[4*i+3] += f[1] / self.corps[i].m # d(vy1)/dt += Fy(2->1)
                dz[4*j+1] -= f[0] / self.corps[j].m # d(vx2)/dt += Fx(1->2) = -Fx(2->1)
                dz[4*j+3] -= f[1] / self.corps[j].m # d(vy2)/dt += Fy(1->2) = -Fy(2->1)

        return dz

    def iteration (self, dt, n) :
        """Iteration de l'état du système"""

        z = []

        for corps in self.corps :
            z += [corps.x, corps.vx, corps.y, corps.vy]

        vect_t = [ i*dt for i in range(n+1) ]

        z = odeint(self.vect_deriv, z, vect_t) # Intègre le système aux instants de vect_t

        # On réinjecte le résultat dans les corps
        for i in range(self.n) :
            self.corps[i].x = z[n][4*i]
            self.corps[i].vx = z[n][4*i+1]
            self.corps[i].y = z[n][4*i+2]
            self.corps[i].vy = z[n][4*i+3]

    def positions (self) :
        """Renvoie la liste des positions des corps du système"""

        z = [[],[]]

        for corps in self.corps :
            z[0] += [corps.x]
            z[1] += [corps.y]

        return z
