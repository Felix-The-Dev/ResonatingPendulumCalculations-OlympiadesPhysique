import tkinter as tk
import random as rd
import numpy as np
import pendule_euler as theory

couleur = ['black', 'white', 'red', 'orange', 'yellow', 'green',
          'turquoise', 'blue', 'purple', 'magenta']
couleur = ["black"]


# Classe principale qui herite de la classe Tk.
class AppliPendule(tk.Tk):
    """Classe principale de l'application (contient la fenetre Tk).
    """

    def __init__(self, l=2e-2, thetadeb=70, alpha=0, f=0, a=0, g=9.81, 
                 tau=1, k=20, tfin=10):
        
        # Appel du constructeur de la classe génitrice.
        # L'instance de la fenetre principale se retrouve dans le self.donc 
        # on pourra le self dans la suite
        tk.Tk.__init__(self)
        
        
        # Etat du mouvement
        self.is_moving = False
        
                
        # ----- Grandeurs physiques initiales -------
        self.t = 0  # temps (s)
        
        
        self.l = l
        self.thetadeb = thetadeb
        self.alpha = alpha
        self.a = a
        self.g = g    # accélération gravitationnelle (m/s^2)
        self.tau = tau
        
        
        # ----- Temps de simulation -----
        tdeb=0
        self.tfin = tfin #date de fin de simulation en seconde en paramètre
        self.k = k # nombre d'occurences de simulation par seconde en paramètre
        self.N = k*tfin # nombre d'occurences de simulation total
        self.dt = (self.tfin-tdeb)/self.N  # intervalle de temps entre chaque simulation (s)
        
        
        self.simulation_being_played = {}
        self.n_playing = 1 # parce que on lui enlève un par la suite      
        
        self.theta = {}
        self.thetap = {}
        self.now_theta = thetadeb/180*np.pi  # angle du pendule
        self.now_thetap = 0.0     # vitesse angulaire ,le pend.ule est au repos au début
        
        self.L = 1  # longueur de la tige  (m)
        self.x = np.sin(self.now_theta) * self.L
        self.y = -np.cos(self.now_theta) * self.L
        # Conversion x, y en coord dans le canevas
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
        
        
        self.canva_reset()
        
        
        
        # Creation des boutons.
        self.btnStart = tk.Button(self, text="Démarrer", command=self.start)
        self.btnStop = tk.Button(self, text="Arreter", command=self.stop)
        
        
        # Création du choix 'direction d'exitation'
        self.alexcit_frame = tk.Frame(self)
        self.alexcit_label = tk.Label(self, text = "Direction d'exitation α =" )
        self.alpha_var = tk.IntVar()
        self.alexcit_rad1 = tk.Radiobutton(self.alexcit_frame,text="verticale (0)",variable=self.alpha_var,value=0)
        self.alexcit_rad2 = tk.Radiobutton(self.alexcit_frame,text="horizontale (π/2)",variable=self.alpha_var,value=np.pi/2)
        if (alpha==0):
            self.alexcit_rad1.select()
        elif (alpha>np.pi/2-0.5 and alpha<np.pi/2+0.5):
            self.alexcit_rad2.select()
        
        # Création de l'entrée 'fréquence d'exitation (f)'
        self.fexcit_frame = tk.Frame(self)
        self.f_var = tk.StringVar()
        self.fexcit_label = tk.Label(self.fexcit_frame, text = "Fréquence d'exitation f =" )
        self.fexcit_entry = tk.Entry(self.fexcit_frame, textvariable=self.f_var, width=10)
        self.f_var.set(str(round(f, 5)))
        
        # Création de l'entrée 'amplitude d'exitation (a)'
        self.aexcit_frame = tk.Frame(self)
        self.a_var = tk.StringVar()
        self.aexcit_label = tk.Label(self.aexcit_frame, text = "Amplitude d'exitation a =" )
        self.aexcit_entry = tk.Entry(self.aexcit_frame, textvariable=self.a_var, width=10)
        self.a_var.set(str(round(a, 5)))
        
        # Creation de la règlette
        self.theta_scale = tk.Scale(self, from_=180, to=-180,
                                    resolution=0.5,
                                    command=self.update_theta_scale)
        self.theta_scale.set(thetadeb)
        scale_description = tk.Label(self, text="valeur initiale de theta",
                                     fg="blue")
        
        
        # Creation du bouton "ouvrir les graphiques"
        open_graphic=tk.Button(self, text="Générer le graphique", bg="#b3c2d0", command=self.open_graphics)
        
        # Creationtion d'un Label pour voir les caracteristiques de la Balle.
        # On utilise une Stringvar (permet de mettre à jour l'affichage).
        self.stringvar_pos_display = tk.StringVar()
        display_theta = tk.Label(self, textvariable=self.stringvar_pos_display,
                                 fg="blue", font=("Courier New", 12))
        
        # --- Placement des widgets dans la fenetre Tk. ----
        self.canv.pack(side=tk.LEFT)
        self.btnStart.pack()  # boutton quitter
        self.btnStop.pack()
        display_theta.pack()
        self.alexcit_label.pack()
        self.alexcit_rad1.pack( side = 'left' )
        self.alexcit_rad2.pack(side = 'right')
        self.alexcit_frame.pack()
        self.fexcit_label.pack( side = 'left' )
        self.fexcit_entry.pack(side = 'right')
        self.fexcit_frame.pack()
        self.aexcit_label.pack( side = 'left' )
        self.aexcit_entry.pack(side = 'right')
        self.aexcit_frame.pack()
        open_graphic.pack(side=tk.BOTTOM)
        
        # Puis la règle et sa description.
        scale_description.pack(side=tk.LEFT)
        self.theta_scale.pack(side=tk.RIGHT)
        
        # --- mise à jour ---
        self.stringvar_pos_display.set(self.get_pos_displ())
        
        
    def canva_reset(self):
        if hasattr(self, "canv"):
            # On vide le canva pour éviter le lag
            self.canv.delete('all')
        else:
            # Creation du canevas dans la fenetre.
            self.canv = tk.Canvas(self, bg='gray', height=400, width=400)
            
        # creation du pivot.
        self.canv.create_oval(190, 190, 210, 210, width=1, fill="blue")
        # creation de la balle.
        self.size = 30  # Taille de la balle ds le repère du canvas.
        self.balle = self.canv.create_oval(self.x_c - (self.size / 2),
                                             self.y_c - (self.size / 2),
                                             self.x_c + (self.size / 2),
                                             self.y_c + (self.size / 2),
                                             width=1, fill="blue")
        # Creation de la tige.
        self.tige = self.canv.create_line(200, 200, self.x_c,
                                          self.y_c, fill="blue")
        # Creation d'une ligne
        self.canv.create_line(0, 200, 400, 200, dash=(3, 3))
        self.canv.create_line(200, 0, 200, 400, dash=(3, 3))
        
        

    def get_pos_displ(self):
        """Retourne une chaine avec la position et la vitesse (angulaire) de la balle.
        """
        return "{:>5s} {:>10s}\n{:>5s} {:>10s}\n{:>5.1f} {:>10.1f}".format(
            "theta", "thetap", "(rad)", "(rad/dt)", self.now_theta, self.now_thetap)

    def map_realcoor2canvas(self, x, y):
        # L = 1 m --> 100 pixel dans le canvas.
        conv_factor = 100
        xprime = x * conv_factor + 200
        yprime = -y * conv_factor + 200
        return xprime, yprime

    def update_theta_scale(self, value):
        """mise à jour dela reglette balle qd la reglette est touchée
        """
        # fin du mouvement du pendule.
        self.stop()
        self.now_thetap = 0.0
        # mise à jour du pendule avec la nouvelle valeur.
        self.now_theta = float(value)/180*np.pi
        self.x = np.sin(self.now_theta) * self.L
        self.y = -np.cos(self.now_theta) * self.L
        # Conversion ds le repere du canvas.
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
        # mise à jour des coordonées (balle + tige).
        self.canv.coords(self.balle,
                         self.x_c - (self.size / 2),
                         self.y_c - (self.size / 2),
                         self.x_c + (self.size / 2),
                         self.y_c + (self.size / 2))
        self.canv.coords(self.tige, 200, 200, self.x_c, self.y_c)
        # mise à jour de la zone de texte.
        self.stringvar_pos_display.set(self.get_pos_displ())
        # mise à  0 le temps.
        self.t = 0

    def move(self):
        """deplace la balle ,mets à jour les coordonnées et s'auto-rappelle après 20 ms.
        """
        
        if self.is_moving:
            # Calcul du nouveau now_theta avec la methode Euler semi-implicite..
            # if self.n_playing-1 < len(self.theta):
            self.now_theta = self.theta[self.n_playing-1]
            self.now_thetap = self.thetap[self.n_playing-1]
            self.n_playing+=1
            # else:
            #     self.now_theta = self.theta[len(self.theta)-1]
            #     self.now_thetap = self.thetap[len(self.thetap)-1]
            
            
            
            # Conversion theta -> x & y.
            self.x = np.sin(self.now_theta) * self.L
            self.y = -np.cos(self.now_theta) * self.L
            # Conversion ds le repÃ¨re du canvas.
            self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
            # On met à jour les coordonnées (balle + tige).
            self.canv.coords(self.balle,
                             self.x_c - (self.size / 2),
                             self.y_c - (self.size / 2),
                             self.x_c + (self.size / 2),
                             self.y_c + (self.size / 2))
            self.canv.coords(self.tige, 200, 200, self.x_c, self.y_c)
            
            # presence de la trace au passage de la balle
            self.canv.create_line(self.x_c, self.y_c, self.x_c + 1,
                                  self.y_c + 1, width=4, fill=self.color_trace)
            # On met à jour la zone de texte.
            self.stringvar_pos_display.set(self.get_pos_displ())
            self.t += self.dt
            
            # On refait appel  à la  methode.move().
            if self.is_moving and self.n_playing < len(self.theta)-1:
                self.after(int(self.dt*1000), self.move)  # boucle toutes les x ms

    def start(self):
        """demarrer la simulation
        """
        print("Started simulation with parameters :",
              "{thetadeb=", str(round(self.now_theta, 5)), 
              "; alpha =", str(round(self.alpha_var.get(), 5)),
              "; f =", str(round(float(self.f_var.get()), 5)),
              "; a =", str(round(float(self.a_var.get()), 5)), "}"
             )
        if not self.is_moving:
            self.btnStart['text'] = 'Relancer'
            self.btnStop['state'] = "normal"
                
            self.canva_reset()
            self.now_theta = self.theta_scale.get()
            
            self.simulation_being_played = theory.calc_pendule(
                thetadeb=self.now_theta, 
                alpha=self.alpha_var.get(), 
                f=int(self.f_var.get()),
                a=int(self.a_var.get()),
                output=["t", "theta", "thetap", "f", "fmin", "N"]
            )
            # self.dt = 0.05 par défaut
            self.theta = self.simulation_being_played["theta"][::int(self.simulation_being_played["N"]/self.N)]
            self.thetap = self.simulation_being_played["thetap"][::int(self.simulation_being_played["N"]/self.N)]
            
            
            self.color_trace = rd.choice(couleur) #choix d'une couleur dans la liste couleur de facon aleatoire
            
            
            self.n_playing = 1
            self.is_moving = True
            # on appele la fonction move une seule fois
            if self.is_moving:
                self.move()
        else:
            self.stop()
            self.after(2*int(self.dt*1000), self.start)

    def stop(self):
        """mettre fin à la simulation
        """
        print("Stopped simulation")
        if self.is_moving :
            self.btnStart['text'] = 'Démarrer'
            self.btnStop['state'] = "disabled"
            self.is_moving = False
            
    def open_graphics(self):
        t_and_theta = theory.calc_pendule(thetadeb=self.now_theta, output=["t", "theta"])
        theory.plot_pendule_evolution(*tuple(t_and_theta.values()))


if __name__ == "__main__":
    simu_pendule = AppliPendule()
    simu_pendule.title("Simulation d'un pendule avec excitation : le phénomène de résonnance")
    simu_pendule.mainloop()
