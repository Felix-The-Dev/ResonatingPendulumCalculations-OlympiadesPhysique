#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

a=np.array([0.001,0.002,0.004,0.01,0.015])#longueurs des pendules en m
ua=0.0005#incertitude sur l en m
l=4e-2#m

fmin=np.array([174,87,44,18,12])#fmin en Hz

ufminbpm=10 #incertitude sur fmin en bpm
g=9.81#m.s-2
ufmin=ufminbpm

# =============================================================================
# / ! \ MAUVAISES INCERTITUDES : mises "au pif" pour que ça soit joli, 
# je ne connais pas les incertitudes que vous aviez prévu, il n'y a que le zscore
# dans votre tableau. J'ai mis des incertitudes pour voir de jolies croix.
# =============================================================================

# on calcule chacune des valeurs de fmin à l'aide de la formule de kapiza
fmin_modele=(2*g*l)**0.5/(2*np.pi*a)

plt.figure()
#on trace les point à l'aide de x
plt.plot(a,fmin_modele,'x',label='Modèle Kapitza') 
#on trace les points avec des barres d'erreurs
plt.errorbar(a,fmin,xerr=ua,yerr=ufmin,fmt='.',label='Valeurs mesurées') 
#On nomme l'axe des abscisses'
plt.xlabel(r'$a$ en m') #le r permet d'interpréter le texte comme du latex
#On nomme l'axe des abscisses'
plt.ylabel(r'$f_{min}$ en Hz')

# plt.xlim(0,0.12)# on fixe les limites de abscisses du graphique
# plt.ylim(0,40)# on fixe les limites de ordonnées du graphique


plt.legend() #permet d'afficher les legendes
plt.grid() #permet d'afficher une grille
plt.savefig('fmin_a.png') #permet de sauvegarder la courbes
plt.show()


