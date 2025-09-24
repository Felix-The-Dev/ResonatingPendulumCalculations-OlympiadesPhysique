"""

Tester :
    
    t_and_theta = calc_pendule(output=["t", "theta"])
    plot_pendule_evolution(*tuple(t_and_theta.values()))

Ne pas oublier l'opérateur d'unpacking du tuple : *

"""


import numpy as np
import matplotlib.pyplot as plt

def calc_pendule(l=2e-2, thetadeb=170, alpha=0, f=51, a=2e-3, g=9.81, tau=1, 
                 N=100000, tfin=10, output=["t", "theta"]):
    """
    Calcule l'évolution de l'angle d'un pendule par rapport à '
    
    @arg l : la longueur du pendule en m
    @arg thetadeb : angle initial du pendule par rapport à la verticale 
                    descendante en degrès (angle de lâché)
    
    
    @arg alpha : angle que fait la direction d'excitation avec la verticale 
                (en radiants: 0 pour vertical, np.pi/2 pour l'horizontale)
    @arg f : fréquence de l'excitateur en Hz
    @arg a : amplitude des excitation en m
    
    
    @arg g : attraction terrestre en m/s^2
    
    @arg tau : temps de relaxation en s (représente les forces de frottement)
    
    @arg N : nombre d'occurences de simulation
    @arg tfin : date de fin de simulation en seconde
                 
    @output: au choix parmi :
        {
            t : tableau des temps
            theta : tableau des angles par rapport à la verticale descendante en rad
            thetap : tableau des vitesses angulaires en rad/s
            "f": fréquence propre pour le pendule fourni en Hz
            "fmin": fréquence minimale pour le pendule fourni en Hz (kapiza)
        }
    """    
    
    # ----- Temps de simulation ----- 
    tdeb=0
    # tfin = date de fin de simulation en seconde en paramètre
    # N = nombre d'occurences de simulation en paramètre
    dt=(tfin-tdeb)/N
    
    # --- Calcul de la fréquence propre de ce pendule (avec g et l) ---
    f0=1/(2*np.pi)*(g/l)**0.5 
    print('fréquence propre:',f0,'Hz')

    
    
    # --- Omega? ---
    omega=2*np.pi*f
    
    # --- Calcul de la fréquence minimale de ce pendule (avec a) ---
    # seulement si a != 0 car sinon, division par 0
    fmin = 0
    if a != 0:
        fmin=(2*g*l)**0.5/(2*np.pi*a)
        print('fréquence minimale pour le pendule kapiza:',fmin,'Hz')
    
    
    # --- Initialisation des tableaux ---
    t=np.zeros(N)      # initialisation du temps
    theta=np.zeros(N)  # initialisation des valeurs de l'angle du pendule par rapport à la verticale ascendante
    thetap=np.zeros(N) # initialisation des valeurs de la vitesse angulaire du pendule
    
        
    # --- Remplissage des tableaux ---
    thetap[0]=0 #vitesse angulaire initiale en rad/s
    theta[0]=thetadeb/180*np.pi #angle initial par rapport à la verticale descendante
    
    
    # --- Calcul des valeurs de theta et thetap par la méthode d'Euler ----
    for i in range(0,N-1):
        t[i+1]=t[i]+dt
        theta[i+1]=theta[i]+dt*thetap[i] 
        thetap[i+1]=thetap[i]+dt*(-np.sin(theta[i])*g/l+np.sin(theta[i]+alpha)*a*omega**2*np.cos(omega*t[i])/l-thetap[i]/tau)
    
    
    # --- Renvoi de l'output désiré ----
    all_outputs = {
        "t": t,
        "theta": theta,
        "thetap": thetap,
        "f": f,
        "fmin": fmin,
        "dt": dt
        }    
    out = {}
    for x in output:
        if x in ["t", "theta", "thetap", "f", "fmin", "dt"] :
            out[x] = all_outputs[x]
        else:
            raise ValueError(f"Unknown output name : {output}")
    return out


def plot_pendule_evolution(t, theta):
    """
    Permet de tracer l'evolution de l'angle du pendule par rapport à la 
    verticale descendante
    """
    plt.figure()
    plt.xlabel('t(s)')
    plt.ylabel(r'$\theta(rad)$')
    plt.grid()
    plt.plot(t,theta)
    plt.show()
    
    
    
    
    
    
if __name__ == '__main__':    
    
    t_and_theta = calc_pendule(output=["t", "theta"])
    plot_pendule_evolution(*tuple(t_and_theta.values()))
    
    
        
