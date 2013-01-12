#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "Time-stamp: <2013-01-12 17:30:19 bpagani>"
__author__ = "Bruno Pagani <bruno.n.pagani@gmail.com>"

"""
Fichier principal du projet, qui utilise les autres pour afficher la simulation.
"""

# On importe le fichier de la classe Systeme
from systeme import *

# Parser du fichier de configuration du systeme
def parse (file) :
    """
    On parse le fichier de configuration du système afin de générer celui-ci.
    """
    

if __name__=='__main__':

    from optparse import OptionParser

    desc = u"Simulation numérique d'un problème N-corps."

    # Définition des options
    parser = OptionParser(usage="%prog [options]",
                          version=__version__, description=desc)
    parser.add_option("-s", "--systeme", type=str, default="example.txt",
                      help=u"Fichier contenant les informations sur le système")
    parser.add_option("-t", "--temps_relatif", type=float, default=1,
                      help=u"Coefficient de dilatation du temps [%default]")
    parser.add_option("-f", "--fps", type=int, default=20,
                      help=u"Nombre d'images par seconde pour l'affichage \
                            [%default fps]")
    parser.add_option("-c", "--calc_per_frame", type=int, default=1,
                      help=u"Nombre de calculs effectués pour chaque image \
                            affichée [%default]")
    parser.add_option("-m", "--method", type=int, default=0,
                      help=u"Méthode d'itération du système [0,1,2]")
    parser.add_option("-w", "--wait", type=float, default=0.,
                      help=u"Temps d'attente entre chaque image, afin de \
                            synchroniser l'écoulement du temps")
    parser.add_option("-T", "--temps_sys", type=float, default=0.,
                      help=u"Pour faire tourner le système pendant temps_sys \
                            (temps système) et procéder à l'affichage ensuite")

    # Déchiffrage des options et arguments
    opts,args = parser.parse_args()

    # Quelques tests sur les options
    if opts.fps <= 0 :
        parser.error(u"Le nombre d'images par seconde doit être strictement \
                      positif")
    periode_affichage = 1./opts.fps # Inverse du nombre d'images par seconde

    try:
        sysfile = open(opts.systeme)
    except (IOError):
        parser.error(u"Le fichier %s n'existe pas" % opts.systeme)

    temps_relatif = opts.temps_relatif
    if temps_relatif <= 0 :
        parser.error(u"Le coefficient de dilatation du temps doit être \
                      strictement positif")

    calc_per_frame = opts.calc_per_frame
    if calc_per_frame <= 0 :
        parser.error(u"Le nombre de calculs par image doit être strictement \
                      positif")

    method = opts.method
    if not method in {0, 1, 2} :
        parser.error(u"La méthode d'itération doit être 0, 1 ou 2")

    wait = opts.wait
    if wait < 0 :
        parser.error(u"Le temps d'attente entre chaque image doit être \
                      strictement positif")
    # Note : strictement, car si wait = 0, on utilise FuncAnimation avec 
    # l'intervalle classique, puisque c'est le seul cas ou wait ne sert à rien.
    # Donc si l'utilisateur a rentré quelque chose, il cherche à avoir le temps 
    # synchronisé, et par conséquent wait différent de 0.

    temps_sys = opts.temps_sys
    if temps_sys <> 0 :
        if temps_sys < temps_relatif * periode_affichage :
            parser.error(u"Le temps d'évolution du système doit être supérieur \
                          à %.2f fois le coefficient de dilation du temps" 
                          % periode_affichage)

    # systeme = parse(sysfile)
    # Création du système - Version temporaire pour les tests, prochainement lecture depuis un fichier
    systeme = Systeme([['Soleil','jaune',0,0,0,0,1.392684e9/2,1.9891e30],['Terre','bleu',1.495978875e11,0,0,29783,6.3710e6,5.9736e24]])

    
    # On importe la fonction d'animation
    from animation import animation
    # Et c'est parti pour le show !
    animation (systeme, periode_affichage, temps_relatif, wait, 
               calc_per_frame, method, temps_sys)
