from math import pi
import numpy as np

def calc_pendule(l, alpha):
    """
    @arg l: longueur du pendule
    @arg alpha: angle du pendule
    @output:    
    """    


    if alpha == "haut" or alpha == "bas" or alpha == "vertical":
        alpha = 0


    elif alpha == "gauche" or alpha == "droite" or alpha == "horizontal":
        alpha = pi/2
