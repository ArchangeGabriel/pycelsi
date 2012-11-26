#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier de classe des objets célestes
"""

class Corps(object) :
    """
    Classe de représentation des objets célestes
    """

    def __init__(self, x, y, r, m) :
        """Initialisation d'un corps"""

        self.x = x
        self.y = y
        self.r = r
        self.m = m

    def __str__(self) :
        """Surcharge de l'opérateur str() pour le classe Corps"""

        chaine_x = "La coordonnée x du corps est : " + str(self.x)
        chaine_y = "La coordonnée y du corps est : " + str(self.y)
        chaine_r = "Le rayon du corps est : " + str(self.r) + " m"
        chaine_m = "La masse du corps est : " + str(self.m) + " kg"

        chaine = ""

        for i in (chaine_x, chaine_y, chaine_r) :
            chaine += i + "\n"

        chaine += chaine_m

        return chaine
