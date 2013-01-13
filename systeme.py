#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "Time-stamp: <2013-01-13 13:52:00 bpagani>"
__author__ = "Bruno Pagani <bruno.n.pagani@gmail.com>"

"""
Fichier de classe du système de corps.
"""

# On importe le fichier de la classe Corps
from corps import *

# On importe la fonction odeint de scipy pour l'intégration numérique
from scipy.integrate import odeint

# On définit la classe Systeme des système de corps
class Systeme (object) :
    """
    Classe de représentation d'un système de corps.
    """

    def __init__ (self, l) :
        """
        Instanciation d'un système à partir d'une liste de corps.
        """

        self.corps = []

        self.n = 0 # Nombre de corps dans le système

        self.E_T = 0 # Énergie cinétique totale du système, initialisée à 0
        self.E_V = 0 # Énergie potentielle totale du système, initialisée à 0

        for corps in l :
            self.corps += [Corps(corps[0], corps[1], corps[2], corps[3], 
                           corps[4], corps[5], corps[6], corps[7])]
            self.n += 1

        # Données d'initialisation pour pouvoir réinitialiser le système
        self.start = l


    def __str__ (self) :
        """
        Surcharge de l'opérateur str() pour la classe Systeme.
        """

        chaine = ""

        for corps in self.corps :
            chaine += str(corps) + "\n"

        return chaine


    def reset (self) :
        """
        Réinitialisation du système.
        """

        self.__init__(self.start)


    def write (self, filename) :
        """
        Ecriture du système dans un fichier.
        """

        outfile = open(filename, 'w')
        outfile.write(str(self))
        outfile.close()


    def vect_deriv (self, z, t) :
        """
        Vecteur des relations dérivées sur x, vx, y, vy.
        """

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
                Vf = self.corps[i].potentiel_force(self.corps[j])
                self.E_V += Vf[0] # E_V = E_V(1) + ... + E_V(n)
                f = Vf[1]
                dz[4*i+1] += f[0] / self.corps[i].m # d(vx1)/dt += Fx(2->1)
                dz[4*i+3] += f[1] / self.corps[i].m # d(vy1)/dt += Fy(2->1)
                dz[4*j+1] -= f[0] / self.corps[j].m # d(vx2)/dt += -Fx(2->1)
                dz[4*j+3] -= f[1] / self.corps[j].m # d(vy2)/dt += -Fy(2->1)

        return dz


    def iteration (self, dt, n) :
        """
        Iteration de l'état du système.
        """

        z = []

        for corps in self.corps :
            z += [corps.x, corps.vx, corps.y, corps.vy]

        vect_t = [ i*dt for i in range(n+1) ]

        # Intègration du système aux instants de vect_t
        z = odeint(self.vect_deriv, z, vect_t)

        # On réinjecte le résultat dans les corps
        for i in range(self.n) :
            self.corps[i].x = z[n][4*i]
            self.corps[i].vx = z[n][4*i+1]
            self.corps[i].y = z[n][4*i+2]
            self.corps[i].vy = z[n][4*i+3]


    def iteration2 (self, dt, n) :
        """
        Iteration de l'état du système.
        """

        z = []

        for corps in self.corps :
            z += [corps.x, corps.vx, corps.y, corps.vy]

        # On intègre n fois le système de dt en le réinjectant dans lui-même
        for i in range(n) :
            z = odeint(self.vect_deriv, z, [0, dt])[1]

        # On réinjecte le résultat dans les corps
        for i in range(self.n) :
            self.corps[i].x = z[4*i]
            self.corps[i].vx = z[4*i+1]
            self.corps[i].y = z[4*i+2]
            self.corps[i].vy = z[4*i+3]


    def positions (self) :
        """
        Renvoie la liste des positions des corps du système.
        """

        z = [[],[]]

        for corps in self.corps :
            z[0] += [corps.x]
            z[1] += [corps.y]

        return z


    def iter1 (self, dt, calc_per_frame, n) :
        """
        Itération complète du système - Version lente. Conserve bien l'énergie, 
        d'autant plus que le nombre de calculs par image est élevé. Pour un 
        calcul par image, même perte que la méthode propre, ce qui est logique 
        étant donné que cela revient strictement au même.
        """
        sys = []

        for i in range(n) :
            for j in range(calc_per_frame):
                self.iteration(dt, 1)
            sys.append(self.positions()+[self.E_T+self.E_V])

        return sys


    def iter2 (self, dt, calc_per_frame, n) :
        """
        Itération complète du système - Version intermédiaire. Devrait 
        fonctionner exactement comme iter1 mais en plus rapide, seulement semble
        fonctionner comme iter3.
        """
        sys = []

        for i in range(n) :
            self.iteration2(dt, calc_per_frame)
            sys.append(self.positions()+[self.E_T+self.E_V])

        return sys


    def iter3 (self, dt, calc_per_frame, n) :
        """
        Itération complère du système - Version propre. Beaucoup plus rapide, 
        mais conserve mal l'énergie. D'ailleurs, il semblerait que la perte 
        d'énergie ne dépende pas du nombre de calculs par image.
        """

        sys = []

        for i in range(n) :
            self.iteration(dt, calc_per_frame)
            sys.append(self.positions()+[self.E_T+self.E_V])

        return sys


    def itern (self, dt, calc_per_frame, n, method=0) :
        """
        Méta-fonction qui appelle la méthode [method] d'itération.
        """

        if not method :
            sys = self.iter1(dt, calc_per_frame, n)
        elif method == 1 :
            sys = self.iter2(dt, calc_per_frame, n)
        elif method == 2 :
            sys = self.iter2(dt, calc_per_frame, n)
        else :
            raise ValueError("method = %d <> 0, 1 ou 2" % method)

        return sys
