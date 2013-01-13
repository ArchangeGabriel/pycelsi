#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "Time-stamp: <2013-01-13 13:50:15 bpagani>"
__author__ = "Bruno Pagani <bruno.n.pagani@gmail.com>"

"""
Fichier de classe des objets célestes.
"""

def norme (v) :
    """
    Renvoie la norme du vecteur v.
    """

    return ( v[0]**2 + v[1]**2 )**.5

class Corps (object) :
    """
    Classe de représentation des objets célestes.
    """

    def __init__ (self, name, colour, x, y, vx, vy, r, m) :
        """
        Instanciation d'un corps.
        """

        self.name = name
        self.colour = colour
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m

    def __str__ (self) :
        """
        Surcharge de l'opérateur str() pour la classe Corps.
        """

        chaine_n = "Corps : " + self.name
        chaine_c = "Couleur : " + self.colour
        chaine_x = "x : " + str(self.x) + " m"
        chaine_y = "y : " + str(self.y) + " m"
        chaine_vx = "vx : " + str(self.vx) + " m.s⁻¹"
        chaine_vy = "vy : " + str(self.vy) + " m.s⁻¹"
        chaine_r = "r : " + str(self.r) + " m"
        chaine_m = "m : " + str(self.m) + " kg"

        chaine = ""

        for i in (chaine_n, chaine_c, chaine_x, chaine_y, 
                  chaine_vx, chaine_vy, chaine_r, chaine_m) :
            chaine += i + "\n"

        return chaine

    def vect (self, corps) :
        """
        Vecteur allant de self à corps.
        """

        return (corps.x - self.x, corps.y - self.y)

    def potentiel_force (self, corps) :
        """
        Potentiel et force exercée par corps sur self.
        """

        corps_k = self.vect(corps)

        # G = 6.67384e-11 m³.kg⁻¹.s⁻²
        V = - 6.67384e-11 * self.m * corps.m / norme(corps_k)

        g = - V / norme(corps_k)**2

        return (V, (g * corps_k[0], g * corps_k[1]))

    def energie_ki (self):
        """
        Energie cinétique du corps.
        """

        return self.m * ( self.vx**2 + self.vy**2 ) / 2
