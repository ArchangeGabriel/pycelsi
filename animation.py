import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

#on cree la figure qui sera affichee.
fig = pyplot.figure()
ax = fig.add_subplot(111, aspect = 'equal', autoscale_on = autoscale) #je me demande s'il faudrait rajouter des xlim et ylim. Essayons d'abord sans.

univers, = ax.plot([], [], 'bo', ms=5) #On affiche un systeme vide qui sera modifie par les fonctions ulterieures au cours de l'animation. En fait on cree ici notre univers visuel.
energie_texte = ax.text(0.02, 0.90, '', transform=ax.transAxes) #voici le texte qui affichera l'energie du systeme et qui sera mis a jour a chaque frame. Si le nombre affiche bouge, nous sommes dans de beaux draps (conservation de l'energie du systeme en theorie).


def initialisation():
	"""
	Donne les prarmetres de départ de l'animation.
	"""
	univers.set_data([], []) #on initialise le systeme avec... rien. Une etape necessaire a l'animation
	energie_texte.set_text('') #on initialise l'affichage l'energie avec rien. Necessaire a l'animation
	
	return univers, energie_texte #on retourne les objets qui seront modifies par l'animation a chaque frame.

def animer(i):
	"""
	Genere l'animation de la frame i en actualisant les positions de la frame i-1.
	"""
	global systeme, dt #on recupere le systeme et la duree entre deux frames
    systeme.avancer(dt) #on actualise les positions du systeme

    univers.set_data(*systeme.position()) #on actualise les positions dans les donnees a afficher. L'etoile specifie a la methode qu'on utilise un argument qui a un nom. Sinon elle crie.
    energie_texte.set_text('energie = %.3f J' % systeme.energie()) #on affiche la nouvelle energie. J'ai pense que 3 chiffres significatifs suffisaient mais si tu veux en rajouter, fais-toi plaisir.

	return univers, energie_texte

#on fixe ensuite l'intervalle en fonction de dt et de la duree separant deux frames. Du gros repompe de GitHub, mais on va voir comment ca se comporte.
import time
t0 = time.time()
animer(0)
t1 = time.time()
intervalle = 1000 * dt - (t1 - t0) #ai pas compris ca. A examiner de plus pres. On peut peut-etre balancer un intervalle arbitraire pour simplifier.


if __name__=="__main__": #partie a utiliser pour les test

anim = animation.FuncAnimation (fig, animer, frame=300, interval=intervalle, blit=True, init_func=initialisation())

pyplot.show()
