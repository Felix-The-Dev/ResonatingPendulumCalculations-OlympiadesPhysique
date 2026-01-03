#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def pendule(f,a,l,alpha,theta0,thetap0=0,tau=4,tdeb=0,tfin=10,N=10000):
    dt=(tfin-tdeb)/N
    g=9.81#m/s2
    omega=2*np.pi*f
    
    tau=4#temps de relaxation en s
    
    t=np.zeros(N)
    theta=np.zeros(N) #initialisation des valeurs de l'angle du pendule par rapport à la verticale ascendante
    thetap=np.zeros(N) #initialisation des valeurs de la vitesse angulaire du pendule
    
    
    thetap[0]=thetap0# vitesse angulaire initiale en rad/s
    theta[0]=theta0 #angle initial par rapport à la verticale descendante
    
    #calcul des valeurs de theta et thetap par la méthode d'Euler
    for i in range(0,N-1):
        t[i+1]=t[i]+dt
        theta[i+1]=theta[i]+dt*thetap[i] 
        thetap[i+1]=thetap[i]+dt*(-np.sin(theta[i])*g/l+np.cos(theta[i]+alpha)*a*omega**2*np.cos(omega*t[i])/l-thetap[i]/tau)
    
    return  t,theta


# ===========================HAWAÏENNE=========================================
alpha=0
l=4e-2
ftab=np.linspace(0.5,6,100)
a=1e-3
theta0=0.0
thetamtab=[]
for f in ftab:
    t,theta=pendule(f,a,l,alpha,theta0)
    thetam=np.max(theta)
    thetamtab.append(thetam)
    print(f,thetam)
#Permet de tracer l'evolution de l'angle du pendule par rapport à la verticale descendante
plt.figure()
plt.xlabel('f(Hz)')
plt.ylabel(r'$\theta_{max}(rad)$')
plt.grid()
plt.plot(ftab,thetamtab)

plt.savefig('thetamax_hawaienne_f.svg')
plt.show()
# =============================================================================




# ===========================QUEUE DE CHEVAL===================================
alpha=np.pi/2
l=4e-2
ftab=np.linspace(0.5,6,100)
a=1e-3
theta0=0.1
thetamtab=[]

for f in ftab:
    t,theta=pendule(f,a,l,alpha,theta0)
    thetam=np.max(theta)
    print(f,thetam)
    thetamtab.append(thetam)
   

plt.figure()
plt.xlabel('f(Hz)')
plt.ylabel(r'$\theta_{max}(rad)$')
plt.grid()
plt.plot(ftab,thetamtab)

plt.savefig('thetamax_queue_cheval_f.svg')
plt.show()
# =============================================================================





# ========================KAPITZA==============================================
alpha=np.pi/2
l=4e-2
ftab=np.linspace(20,40,100)
a=5e-3
theta0=170/180*np.pi
thetamtab=[]
for f in ftab:
    t,theta=pendule(f,a,l,alpha,theta0)
    thetam=np.mean(theta)
    print(f,thetam)
    thetamtab.append(thetam)
    
# Permet de tracer l'evolution de l'angle du pendule par rapport à la verticale descendante
plt.figure()
plt.xlabel('f(Hz)')
plt.ylabel(r'$\theta_{moy}(rad)$')
plt.grid()
#on trace les points avec des barres d'erreurs
plt.errorbar(ftab,thetamtab,xerr=ua,yerr=ufmin,fmt='.',label='Valeurs mesurées') 
plt.savefig('thetamoy_kapitza_f.svg')

plt.show()
# =============================================================================








