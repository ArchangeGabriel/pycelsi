#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier de classe des objets célestes
"""

class Corps(object) :
    """
    Classe de représentation des objets célestes
    """

    def __init__(self, x, y, vx, vy, r, m, name = "Corps") :
        """Instanciation d'un corps"""

        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m

    def __str__(self) :
        """Surcharge de l'opérateur str() pour le classe Corps"""

        chaine_name = "Ce corps s'appelle %s" % self.name
        chaine_x = "La coordonnée x du corps est : " + str(self.x)
        chaine_y = "La coordonnée y du corps est : " + str(self.y)
        chaine_vx = "La composante x de la vitesse du corps est : " + str(self.vx) + " m.s⁻¹"
        chaine_vy = "La composante y de la vitesse du corps est : " + str(self.vy) + " m.s⁻¹"
        chaine_r = "Le rayon du corps est : " + str(self.r) + " m"
        chaine_m = "La masse du corps est : " + str(self.m) + " kg"

        chaine = ""

        for i in (chaine_name, chaine_x, chaine_y, chaine_vx, chaine_vy, chaine_r) :
            chaine += i + "\n"

        chaine += chaine_m

        return chaine

    def vect(self, corps) :
        """Vecteur allant de self à corps"""

        return (corps.x - self.x, corps.y - self.y)
