"""
Fonctions :
1 - calc_pendule
Calcule l'évolution de l'angle d'un pendule soumis ou non à un excitation 
verticale ou  horizontale. Calcule également la fréquence propre du pendule
donné et le renvoie si demandé en output.

2 - calc_f0
Calcule seulement la fréquence propre f0 d'un pendule de longueur l soumis
à une attraction terrestre g
    
3 - plot_pendule_evolution
Permet de tracer l'evolution de l'angle du pendule par rapport à la
verticale descendante
"""


import numpy as np
import matplotlib.pyplot as plt
import math

def calc_pendule(l=5e-2, thetadeb=160, alpha=0, f=0, a=0, g=9.81, tau=1,
                 k=10000, tfin=20, output=["t", "theta"]):
    """
    Calcule l'évolution de l'angle d'un pendule soumis ou non à un excitation 
    verticale ou  horizontale. Calcule également la fréquence propre du pendule
    donné et le renvoie si demandé en output.

    @arg l : la longueur du pendule en m
    @arg thetadeb : angle initial du pendule par rapport à la verticale
                    descendante en degrès (angle de lâché)


    @arg alpha : angle que fait la direction d'excitation avec l'horizontale
                (en radiants: np.pi/2 pour vertical, 0 pour l'horizontale)
    @arg f : (51) fréquence de l'excitateur en Hz
    @arg a : (2e-3) amplitude des excitation en m


    @arg g : attraction terrestre en m/s^2

    @arg tau : temps de relaxation en s (représente les forces de frottement)

    @arg k : nombre d'occurences de simulation par seconde
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
    # k = nombre d'occurences de simulation par seconde
    N = k * tfin # nombre total d'occurences de simulation
    dt=(tfin-tdeb)/N

    # --- Calcul de la fréquence propre de ce pendule (avec g et l) ---
    f0=1/(2*np.pi)*(g/l)**0.5
    # print('fréquence propre:',f0,'Hz')



    # --- Omega? ---
    omega=2*np.pi*f

    # --- Calcul de la fréquence minimale de ce pendule (avec a) ---
    # seulement si a != 0 car sinon, division par 0
    fmin = 0
    if a != 0:
        fmin=(2*g*l)**0.5/(2*np.pi*a)
        # print('fréquence minimale pour le pendule kapiza:',fmin,'Hz')


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
        thetap[i+1]=thetap[i]+dt*(-np.sin(theta[i])*g/l+np.cos(theta[i]+alpha)*a*omega**2*np.cos(omega*t[i])/l-thetap[i]/tau)


    # --- Renvoi de l'output désiré ----
    all_outputs = {
        "t": t,
        "theta": theta,
        "thetap": thetap,
        "f0": f0,
        "fmin": fmin,
        "N": N
        }
    out = {}
    for x in output:
        if x in ["t", "theta", "thetap", "f0", "fmin", "N"] :
            out[x] = all_outputs[x]
        else:
            raise ValueError(f"Unknown output name : {output}")
    return out

def calc_f0(l, g):
    """
    Calcule seulement la fréquence propre f0 d'un pendule de longueur l soumis
    à une attraction terrestre g
    
    @arg l : la longueur du pendule en m
    @arg g : attraction terrestre en m/s^2
    """
    
    f0=1/(2*np.pi)*(g/l)**0.5
    return f0


def calc_fmin(l, g, a):
    """
    Calcule seulement la fréquence minimale de Kapiza fmin d'un pendule de longueur l soumis
    à une attraction terrestre g et excité avec une amplitude a
    
    @arg l : la longueur du pendule en m
    @arg g : attraction terrestre en m/s^2
    """
    if a == 0:
        return None
    else:
        fmin=(2*g*l)**0.5/(2*np.pi*a)
        return fmin
    


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


def calc_excitation(f, a, tfin, N):
    """
        Crée un tableau numpy contenant la valeur de décalement à effectuer pour le
        pivot pour qu'on ait visuellement l'impression que l'excitation a lieu
        sur la simulation.
        
        f=5 est une fréquence maximum pourqu'on voit l'excitation sans rendre 
        la simulation trop disgracieuse (avec une grande amplitude, c'est à vomir xD)
        à partir de f=10, on ne voit même plus le changement de position
        
    """
    
    # décalage à appliquer en x ou en y suivant le cas
    dec=np.zeros(N)
    
    if f==0 or a==0: #éviter les divisions par 0
        return dec
    else:
            
        tdeb = 0 
        dt=(tfin-tdeb)/N     # temps entre chaque occurence de simulation
        
        T = 1/f              # période
        
        
        b= (2*np.pi) / T     # coefficient de x dans la formule du sinus
          
        
        for x in range(N): 
            dec[x] = a*math.sin(b*(x*dt))
        
        return dec
        
        
    





if __name__ == '__main__':
    
    t, theta = tuple(calc_pendule(l=5e-2, thetadeb=45, alpha=0, f=5, a=1e-2, g=9.81, tfin=10, output=["t", "theta"]).values())
    plot_pendule_evolution(t, theta)



