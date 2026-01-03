#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib_inline.backend_inline import set_matplotlib_formats
set_matplotlib_formats('svg')

l=np.array([2e-2,4e-2,6e-2,8e-2,10e-2])#longueurs des pendules en m
invsrqtl=1/np.sqrt(l)
f=np.array([3.546,2.591,2.058,1.751,1.567]) # f en Hz

u_invsqrtl=np.array([0.18,0.062,0.034,0.022,0.016])#incertitude sur l en m
u_f=np.array([0.044,0.025,0.016,0.011,0.0088])#incertitude sur f en Hz


plt.figure()

#on trace la droite linéaire formée par les points

# =============================================================================
#        # ajustement linéaire
#        a, b = np.polyfit(invsrqtl, f, 1)
# Coefficients données par Regressi
a, b = 0.499, 0
# =============================================================================

droite = a * invsrqtl + b           # calcul des valeurs ajustées



#on trace les points expérimentaux avec des barres d'erreurs
plt.errorbar(invsrqtl,f,xerr=u_invsqrtl,yerr=u_f,fmt='o',label='Valeurs mesurées')       
plt.plot(invsrqtl, droite, '-', label='Ajustement linéaire')  # droite ajustée

print(r"L'équation de la courbe est $f_0$ =", round(a, 5), "1/sqrt(l)")
plt.text(3.75, 3.80, r"L'équation de la courbe est : $f_0$ = " + str(round(a, 5)) + r" $\frac{1}{\sqrt{l}}$")

#On nomme l'plte des abscisses'
plt.xlabel(r'$\frac{1}{\sqrt{l}}$ en m') #le r permet d'interpréter le texte comme du latex
#On nomme l'plte des abscisses'
plt.ylabel(r'$f_0$ en Hz')

# plt.xlim(0,0.12)# on fixe les limites de abscisses du graphique
# plt.ylim(0,40)# on fixe les limites de ordonnées du graphique


plt.legend() #permet d'afficher les legendes
plt.grid() #permet d'afficher une grille
plt.savefig('invsqrtl.svg') #permet de sauvegarder la courbes
plt.show()


