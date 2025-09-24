#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 16:57:46 2025

@author: stephanebelin
"""
import numpy as np
import matplotlib.pyplot as plt
tdeb=0
tfin=10 #date de fin en seconde
N=100000
dt=(tfin-tdeb)/N

alpha=0#np.pi/2 #angle que fait la direction d'excitation avec la verticale
l=2e-2# longueur du pendule en m
g=9.81#m/s2
f0=1/(2*np.pi)*(g/l)**0.5
print('fréquence propre:',f0,'Hz')

f=51# fréquence de l'excitateur en Hz
omega=2*np.pi*f
a=2e-3#amplitude des oscillations en m
fmin=(2*g*l)**0.5/(2*np.pi*a)
print('fréquence minimale pour le pendule kapiza:',fmin,'Hz')

tau=1#temps de relaxation en s

t=np.zeros(N)
theta=np.zeros(N) #initialisation des valeurs de l'angle du pendule par rapport à la verticale ascendante
thetap=np.zeros(N) #initialisation des valeurs de la vitesse angulaire du pendule


thetap[0]=0# vitesse angulaire initiale en rad/s
theta[0]=170/180*np.pi #angle initial par rapport à la verticale descendante

#calcul des valeurs de theta et thetap par la méthode d'Euler
for i in range(0,N-1):
    t[i+1]=t[i]+dt
    theta[i+1]=theta[i]+dt*thetap[i] 
    thetap[i+1]=thetap[i]+dt*(-np.sin(theta[i])*g/l+np.sin(theta[i]+alpha)*a*omega**2*np.cos(omega*t[i])/l-thetap[i]/tau)

#Permet de tracer l'evolution de l'angle du pendule par rapport à la verticale descendante
plt.figure()
plt.xlabel('t(s)')
plt.ylabel(r'$\theta(rad)$')
plt.grid()
plt.plot(t,theta)
plt.show()
