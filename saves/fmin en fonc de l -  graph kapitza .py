#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

l=np.array([2e-2,4e-2,6e-2,8e-2,10e-2])#longueurs des pendules en m
fminbpm=np.array([1000,1200,1400,1500,1740])#fmin en bpm

ul=2e-3#incertitude sur l en m
ufminbpm=100#incertitude sur fmin en bpm
a=6e-3#m
g=9.81#m.s-2

fmin=fminbpm/60

ufmin=ufminbpm/60

# =============================================================================
# / ! \ MAUVAISES INCERTITUDES : mises "au pif" pour que ça soit joli, 
# je ne connais pas les incertitudes que vous aviez prévu, il n'y a que le zscore
# dans votre tableau. J'ai mis des incertitudes pour voir de jolies croix.
# =============================================================================

# on calcule chacune des valeurs de fmin à l'aide de la formule de kapiza
fmin_modele=(2*g*l)**0.5/(2*np.pi*a)

plt.figure()
#on trace les point à l'aide de x
plt.plot(l,fmin_modele,'x',label='Modèle Kapitza') 
#on trace les points avec des barres d'erreurs
plt.errorbar(l,fmin,xerr=ul,yerr=ufmin,fmt='.',label='Valeurs mesurées') 
#On nomme l'axe des abscisses'
plt.xlabel(r'$l$ en m') #le r permet d'interpréter le texte comme du latex
#On nomme l'axe des abscisses'
plt.ylabel(r'$f_{min}$ en Hz')

plt.xlim(0,0.12)# on fixe les limites de abscisses du graphique
plt.ylim(0,40)# on fixe les limites de ordonnées du graphique


plt.legend() #permet d'afficher les legendes
plt.grid() #permet d'afficher une grille
plt.savefig('fmin_l.svg') #permet de sauvegarder la courbes
plt.show()


