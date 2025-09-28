"""
Fenêtre tkinter qui permet de calculer f0 et T0 pour un l, g et tau donné et
de visualiser et de tracer le graphique du mouvement d'un pendule avec n'importe 
angle thetadeb initial, fréquence d'excitation et amplitude d'excitation.
Des paramètre prédéfinis peuvent être sélectionnés pour mettre en évidence certains
phénomènes :)
"""
import tkinter as tk
from tkinter import ttk
import random as rd
import numpy as np
import pendule_euler as theory

# Paramètres particuliers que l'utilisateur peut choisir. 
# Il est possible d'insérer des calculs (format python) en utilisant f0 dans une string. 
# Ex: "f" = "f0*2"
# Il est possible de seulement mettre "actuel" comme valeur lorsque ce paramètre n'est pas important pour le cas présent
# Ex: "a" = "actuel"
# /!\ Ne pas supprimer la dernière ligne de texte et son "\n" Elle affichera les valeurs des paramètres
# /!\ Ne pas utiliser de chaine en triple guillemets : ça génère des espaces disgracieux
predefined_settings = [
    {
        "text":"Excitation verticale, pendule en haut avec une excitation de grande fréquence :"+
            "\nLe pendule est maintenu vers le haut"+
            "\n(thetadeb=xx, α=xx, f=xx, a=xx)",
        "parameters":{"thetadeb":115, "alpha":0, "f":51, "a":5e-3}
        # Remarque : à partir de thetadeb = 115, le pendule 6cm se dresse. Sinon il retombe
    },
    { 
        "text":"Excitation horizontale à la fréquence propre du pendule :"+
            "\nLe pendule ocille à une amplitude maximale indéfiniment"+
            "\n(thetadeb=xx, α=xx, f=xx, a=xx)",
        "parameters":{"thetadeb":"actuel", "alpha":np.pi/2, "f":"f0", "a":2e-2}
    }
]



# si on veut changer la couleur de la trainée laissée par le pendule : fun ^u^:
# (pris aléatoirement dans la liste)
couleur = ['black', 'white', 'red', 'orange', 'yellow', 'green',
          'turquoise', 'blue', 'purple', 'magenta']
couleur = ["black"]



# Classe principale qui herite de la classe Tk.
class AppliPendule(tk.Tk):
    """
        Classe principale de l'application (contient la fenetre Tk).
        Pour ouvrir la fenêtre, créer une instance et appliquer la méthode .mainloop()
    """

    def __init__(self, l=6e-2, thetadeb=45, alpha=np.pi/2, f=0, a=0, g=9.81,
                 tau=1, k=20, tfin=20):

        # Appel du constructeur de la classe génitrice.
        # L'instance de la fenetre principale se retrouve dans le self.donc
        # on pourra le self dans la suite
        tk.Tk.__init__(self)
        self.title("Simulation d'un pendule avec excitation : le phénomène de résonnance")
        

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
        self.f0 = 0


        # ----- Temps de simulation -----
        tdeb=0
        self.tfin = tfin #date de fin de simulation en seconde en paramètre
        self.k = k # nombre d'occurences de simulation par seconde en paramètre
        self.N = k*(tfin-tdeb) # nombre d'occurences de simulation total
        self.dt = (self.tfin-tdeb)/self.N  # intervalle de temps entre chaque simulation (s)
        

        self.simulation_being_played = {}
        self.n_playing = 1 # parce que on lui enlève un par la suite

        self.theta = {}
        self.thetap = {}
        self.now_theta = thetadeb/180*np.pi  # angle du pendule
        self.now_thetap = 0.0     # vitesse angulaire ,le pend.ule est au repos au début
        
        
        self.ocil_dec_x = {}
        self.ocil_dec_y = {}
        self.now_ocil_dec_x = 0.0
        self.now_ocil_dec_y = 0.0
        
        self.L = l*100/5  # longueur de la tige  (mesure de tkinter)
        self.x = np.sin(self.now_theta) * self.L
        self.y = -np.cos(self.now_theta) * self.L
        # Conversion x, y en coord dans le canevas
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)



        self.change_pendulum_window = None # variable qui accueillera la fenêtre de modification des paramètres


        self.canva_reset()



        # Creation des boutons.
        self.startstop_frame = tk.Frame(self)
        self.btnStart = tk.Button(self.startstop_frame, text="Démarrer", command=self.start, bg="#CFE3CF")
        self.btnStop = tk.Button(self.startstop_frame, text="Arreter", command=self.stop, bg="#DECBC5")


        # Creationtion d'un Label pour voir les caracteristiques du pendule en temps réel.
        # On utilise une Stringvar (permet de mettre à jour l'affichage).
        self.stringvar_pos_display = tk.StringVar()
        display_theta = tk.Label(self, textvariable=self.stringvar_pos_display,
                                 fg="blue", font=("Courier New", 12))


        # Creation du bouton pour ouvrir la fenêtre des propriétés du pendule
        self.btnChangePendulum = tk.Button(self, text="Modifier les propriétés du pendule", command=self.open_change_pendulum_window)




        # Création du choix 'direction d'excitation'
        self.alexcit_frame = tk.Frame(self)
        self.alexcit_label = tk.Label(self.alexcit_frame, text = "Direction d'excitation α =" )
        self.alpha_var = tk.DoubleVar()
        self.alexcit_rad1 = tk.Radiobutton(self.alexcit_frame,text="verticale (0)",variable=self.alpha_var,value=0)
        self.alexcit_rad2 = tk.Radiobutton(self.alexcit_frame,text="horizontale (π/2)",variable=self.alpha_var,value=np.pi/2)
        self.alpha_var.set(alpha)
        

        # Création de l'entrée 'fréquence d'excitation (f)'
        self.fexcit_frame = tk.Frame(self)
        self.f_var = tk.StringVar()
        self.fexcit_label = tk.Label(self.fexcit_frame, text = "Fréquence d'excitation f =" )
        self.fexcit_entry = tk.Entry(self.fexcit_frame, textvariable=self.f_var, width=10)
        self.f_var.set(str(round(f, 5)))
        self.f_var.trace("w", self.update_ocillation_showing)

        # Création de l'entrée 'amplitude d'excitation (a)'
        self.aexcit_frame = tk.Frame(self)
        self.a_var = tk.StringVar()
        self.aexcit_label = tk.Label(self.aexcit_frame, text = "Amplitude d'excitation a =" )
        self.aexcit_entry = tk.Entry(self.aexcit_frame, textvariable=self.a_var, width=10)
        self.a_var.set(str(round(a, 5)))
        
        # Création de la checkbox "Afficher les ocillations"
        self.show_ocillation_var = tk.BooleanVar()
        self.show_ocillation_checkbox = ttk.Checkbutton(
            self,
            text="Afficher les ocillations",
            variable=self.show_ocillation_var
        )
        self.show_ocillation_var.set(True)
        update_fonc = self.calc_ocillation_to_show
        self.show_ocillation_var.trace("w", update_fonc)


        # Creation de la règlette
        self.theta_scale = tk.Scale(self, from_=180, to=-180,
                                    resolution=1,
                                    command=self.update_theta_scale)
        self.theta_scale.set(thetadeb)
        scale_description = tk.Label(self, text="Valeur initiale de theta :",
                                     fg="blue")
        
        
        # Creation du bouton pour ouvrir la fenêtre des 
        self.btnLoadParameters= tk.Button(self, text="Charger des cas préenregistrés", command=self.open_load_parameters_window)


        # Creation du bouton "ouvrir les graphiques" et de son bouton associé pour voir seulement ce que simule le pendule
        open_graphic_frame = tk.Frame(self)
        open_graphic=tk.Button(open_graphic_frame, text="Générer le graphique", bg="#b3c2d0", command=self.open_graphics, cursor="hand2")
        open_simulation_graphic=tk.Button(open_graphic_frame, text="#", bg="#b3c2d0", command=self.open_simulation_graphics)


        # --- Placement des widgets dans la fenetre Tk. ----
        self.canv.pack(side=tk.LEFT)
        self.btnStart.pack(padx=2, side = 'left')  # boutton quitter
        self.btnStop.pack(padx=2, side = 'right')
        self.startstop_frame.pack()
        display_theta.pack(pady=5)
        self.btnLoadParameters.pack(pady=5)
        self.alexcit_label.pack()
        self.alexcit_rad1.pack(side = 'left')
        self.alexcit_rad2.pack(side = 'right')
        self.alexcit_frame.pack(pady=2)
        self.fexcit_label.pack(side = 'left')
        self.fexcit_entry.pack(side = 'right')
        self.fexcit_frame.pack(pady=2)
        self.aexcit_label.pack( side = 'left')
        self.aexcit_entry.pack(side = 'right')
        self.aexcit_frame.pack(pady=2)
        self.show_ocillation_checkbox.pack(pady=2)
        self.btnChangePendulum.pack()
        
        open_graphic_frame.pack(side=tk.BOTTOM)
        open_graphic.pack(side=tk.LEFT)
        open_simulation_graphic.pack(side=tk.RIGHT)
        

        # Puis la règle et sa description.
        scale_description.pack(side=tk.LEFT)
        self.theta_scale.pack(side=tk.RIGHT)

        # --- mise à jour ---
        self.stringvar_pos_display.set(self.get_pos_displ())
        
        self.after(50, self.start)


    def canva_reset(self):
        if hasattr(self, "canv"):
            # On vide le canva pour éviter le lag
            self.canv.delete('all')
        else:
            # Creation du canevas dans la fenetre.
            self.canv = tk.Canvas(self, bg='gray', height=450, width=450)


        # creation du pivot.
        self.pivot = self.canv.create_oval(215, 215, 235, 235, width=1, fill="blue")
        # creation de la balle.
        self.size = 30  # Taille de la balle ds le repère du canvas.
        self.balle = self.canv.create_oval(self.x_c - (self.size / 2),
                                             self.y_c - (self.size / 2),
                                             self.x_c + (self.size / 2),
                                             self.y_c + (self.size / 2),
                                             width=1, fill="blue")
        # Creation de la tige.
        self.tige = self.canv.create_line(225, 225, self.x_c,
                                          self.y_c, fill="blue")
        # Creation d'une ligne
        self.canv.create_line(0, 225, 475, 225, dash=(3, 3))
        self.canv.create_line(225, 0, 225, 475, dash=(3, 3))



    def get_pos_displ(self):
        """Retourne une chaine avec la position et la vitesse (angulaire) de la balle.
        """
        return "{:>5s} {:>10s}\n{:>5s} {:>10s}\n{:>5.1f} {:>10.1f}".format(
            "theta", "thetap", "(rad)", "(rad/dt)", self.now_theta, self.now_thetap)

    def map_realcoor2canvas(self, x, y):
        # L = 1 m --> 100 pixel dans le canvas.
        conv_factor = 100
        xprime = x * conv_factor + 225
        yprime = -y * conv_factor + 225
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
        self.canv.coords(self.tige, 225, 225, self.x_c, self.y_c)
        # mise à jour de la zone de texte.
        self.stringvar_pos_display.set(self.get_pos_displ())
        # mise à  0 le temps.
        self.t = 0

    def move(self):
        """deplace la balle ,mets à jour les coordonnées et s'auto-rappelle après 20 ms.
        """

        if self.is_moving:
            # On récupère le nouveau now_theta dans self.theta qui contient tous les theta au cours du temps
            
            self.now_theta = self.theta[self.n_playing-1]
            
            self.now_ocil_dec_x = self.ocil_dec_x[self.n_playing-1]
            self.now_ocil_dec_y = self.ocil_dec_y[self.n_playing-1]
            
            self.now_thetap = self.thetap[self.n_playing-1]
            self.n_playing+=1



            # Conversion theta -> x & y.
            self.x = np.sin(self.now_theta) * self.L
            self.y = -np.cos(self.now_theta) * self.L
            # Conversion ds le repÃ¨re du canvas.
            self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
            # On met à jour les coordonnées (balle + tige).
            self.canv.coords(self.balle,
                             self.x_c - (self.size / 2)+self.now_ocil_dec_x*10e2,
                             self.y_c - (self.size / 2)+self.now_ocil_dec_y*10e2,
                             self.x_c + (self.size / 2)+self.now_ocil_dec_x*10e2,
                             self.y_c + (self.size / 2)+self.now_ocil_dec_y*10e2)
            
            self.canv.coords(self.tige, 225+self.now_ocil_dec_x*10e2, 225+self.now_ocil_dec_y*10e2, self.x_c+self.now_ocil_dec_x*10e2, self.y_c+self.now_ocil_dec_y*10e2)
            self.canv.coords(self.pivot, 215+self.now_ocil_dec_x*10e2, 215+self.now_ocil_dec_y*10e2, 235+self.now_ocil_dec_x*10e2, 235+self.now_ocil_dec_y*10e2)

            # presence de la trace au passage de la balle
            self.canv.create_line(self.x_c+self.now_ocil_dec_x*10e2, self.y_c+self.now_ocil_dec_y*10e2, self.x_c+self.now_ocil_dec_x*10e2 + 1,
                                  self.y_c+self.now_ocil_dec_y*10e2 + 1, width=4, fill=self.color_trace)
            
            # On met à jour la zone de texte.
            self.stringvar_pos_display.set(self.get_pos_displ())
            self.t += self.dt

            # On refait appel  à la  methode.move().
            if self.is_moving and self.n_playing < self.N-1:
                self.after(int(self.dt*1000), self.move)  # boucle toutes les x 
            else:
                self.stop()

    def start(self):
        """demarrer la simulation
        """
        print("\nStarted simulation with parameters :\n",
              "{thetadeb=", str(round(self.now_theta, 5)),
              "; alpha =", str(round(self.alpha_var.get(), 5)),
              "; f =", str(round(float(self.f_var.get()), 5)),
              "; a =", str(round(float(self.a_var.get()), 5)),
              "; l =", str(round(float(self.l), 5)),
              "; g =", str(round(float(self.g), 5)),
              "; tau =", str(round(float(self.tau), 5)), 
              "; tfin=", str(round(float(self.tfin), 5)),"}"
             )
        if not self.is_moving:
            self.btnStart['text'] = 'Relancer'
            self.btnStop['state'] = "normal"

            self.canva_reset()
            
            
                    
            
            
            self.simulation_being_played = theory.calc_pendule(
                thetadeb=self.theta_scale.get(),
                alpha=self.alpha_var.get(),
                f=float(self.f_var.get()),
                a=float(self.a_var.get()),
                l = float(self.l),
                g = float(self.g),
                tau = float(self.tau),
                tfin= self.tfin,
                output=["t", "theta", "thetap", "f0", "fmin", "N"]
            )
            # self.dt = 0.05 par défaut
            self.theta = self.simulation_being_played["theta"][::int(self.simulation_being_played["N"]/self.N)]
            self.thetap = self.simulation_being_played["thetap"][::int(self.simulation_being_played["N"]/self.N)]
            
            # On initialise
            self.now_theta = self.theta[0]
            self.calc_ocillation_to_show()
            
            self.f0=self.simulation_being_played["f0"]
            
            # Estethique
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

        if self.is_moving :
            self.btnStart['text'] = 'Démarrer'
            self.btnStop['state'] = "disabled"
            self.is_moving = False
    
    def calc_ocillation_to_show(self, *arg, **kargs):
        # On regarde si on doit afficher les ocillations du pendule ou non
        self.ocil_dec_x = np.zeros(self.N)
        self.ocil_dec_y = np.zeros(self.N)
        
        if self.show_ocillation_var.get(): 
            
            # fréquence maximale de f=3, pour notre santé occulaire xD
            if float(self.f_var.get())>=5:                     
                f=5
            else:
                f=float(self.f_var.get())
                
            if self.alpha_var.get() == 0: # si l'excitation est verticale
               self.ocil_dec_y = theory.calc_excitation(f, float(self.a_var.get()), self.tfin, self.N)
 
            elif self.alpha_var.get() == np.pi/2:  # si l'excitation est horizontale
                self.ocil_dec_x = theory.calc_excitation(f, float(self.a_var.get()), self.tfin, self.N)
             
                
        # on initialise      
        self.now_ocil_dec_x = self.ocil_dec_x[0]
        self.now_ocil_dec_y = self.ocil_dec_y[0]
        
        # Esthetique
        # On suppose la fréquence demandée raisonnablement entre 0.01 et 100 Hz
        if float(self.a_var.get()) != 0:
            if float(self.f_var.get()) <= 0.5:
                self.canv.itemconfigure(self.pivot, fill="#0000ff")
            if float(self.f_var.get()) <= 1:
                self.canv.itemconfigure(self.pivot, fill="#01456c")
            elif float(self.f_var.get()) <= 2:
                self.canv.itemconfigure(self.pivot, fill="#706500")
            elif float(self.f_var.get()) <= 5:
                self.canv.itemconfigure(self.pivot, fill="#7a6100")
            elif float(self.f_var.get()) <= 9.5:
                self.canv.itemconfigure(self.pivot, fill="#734c00")
            else:
                self.canv.itemconfigure(self.pivot, fill="#760000")
        else:
            self.canv.itemconfigure(self.pivot, fill="#0000ff")

    def update_ocillation_showing(self, *arg, **kargs):
        """
            Appellé lorsque f est modifié
        """
        try:
            if float(self.f_var.get())>=5:
                self.show_ocillation_checkbox.config(text="Afficher des ocillations (déconseillé \nlorsque f et a trop grands)")
            else:
                self.show_ocillation_checkbox.config(text="Afficher les ocillations")
        except ValueError:
            self.show_ocillation_checkbox.config(text="Afficher les ocillations")
        
            

    def open_change_pendulum_window(self):
        self.btnChangePendulum['state'] = "disabled"
        
        self.change_pendulum_window = tk.Toplevel()
        self.change_pendulum_window.title("Modifier les propriétés du pendule")
               
        
        self.change_pendulum_window.l_var = tk.StringVar()
        self.change_pendulum_window.l_var.set(str(round(self.l, 5)))
        self.change_pendulum_window.g_var = tk.StringVar()
        self.change_pendulum_window.g_var.set(str(round(self.g, 5)))
        self.change_pendulum_window.tau_var = tk.StringVar()
        self.change_pendulum_window.tau_var.set(str(round(self.tau, 5)))

        # Créer et placer les labels et les champs de saisie
        tk.Label(self.change_pendulum_window, text="Longueur du pendule (m):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        l_entry = tk.Entry(self.change_pendulum_window, textvariable=self.change_pendulum_window.l_var)
        l_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.change_pendulum_window, text="Constante gravitationnelle (m/s²):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        g_entry = tk.Entry(self.change_pendulum_window, textvariable=self.change_pendulum_window.g_var)
        g_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.change_pendulum_window, text="Force de frottement (s):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tau_entry = tk.Entry(self.change_pendulum_window, textvariable=self.change_pendulum_window.tau_var)
        tau_entry.grid(row=2, column=1, padx=10, pady=5)

        update_fonc = self.update_f0
        self.change_pendulum_window.l_var.trace("w", update_fonc)
        self.change_pendulum_window.g_var.trace("w", update_fonc)
        self.change_pendulum_window.tau_var.trace("w", update_fonc)


        self.change_pendulum_window.f0_string_var = tk.StringVar()
        self.change_pendulum_window.f0_string_var.set("Fréquence propre du pendule pour ces conditions f0= "+str(round(self.f0, 5))+"Hz\n"
                                                      + "Période propre du pendule pour ces conditions T0= "+str(round(1/self.f0, 5))+"s" )
        
        tk.Label(self.change_pendulum_window,textvariable=self.change_pendulum_window.f0_string_var).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="e")

        self.change_pendulum_window.protocol("WM_DELETE_WINDOW", self.close_change_pendulum_window)

        # Lancer la boucle principale de la fenêtre
        self.change_pendulum_window.mainloop()
    
    
    def close_change_pendulum_window(self):
        self.btnChangePendulum['state'] = "normal"
        self.change_pendulum_window.destroy()

    def update_f0(self, *arg, **karg):
        self.l = float(self.change_pendulum_window.l_var.get())
        self.g = float(self.change_pendulum_window.g_var.get())
        self.tau = float(self.change_pendulum_window.tau_var.get())
        
        l = self.l
        g = self.g
        tau = self.tau
        # éviter les erreurs de division par 0
        if l == 0:
            l=0.01
        if g == 0:
            l=0.01
        if tau == 0:
            l=0.01
            
        # mise à jour de la longueur de la tige  (mesure de tkinter)
        self.L = l*100/5  
        
        self.simulation_being_played = theory.calc_pendule(
                thetadeb=self.theta_scale.get(),
                alpha=self.alpha_var.get(),
                f=float(self.f_var.get()),
                a=float(self.a_var.get()),
                l = float(l),
                g = float(self.g),
                tau = float(self.tau),
                tfin= self.tfin,
                output=["t", "theta", "thetap", "f0", "fmin", "N"]
            )
        
        self.f0 = self.simulation_being_played["f0"]
        
        self.change_pendulum_window.f0_string_var.set("Fréquence propre du pendule pour ces conditions f0="+str(round(self.f0, 5))+"Hz\n"
                                                      + "Période propre du pendule pour ces conditions T0="+str(round(1/self.f0, 5))+"s" )

    def open_load_parameters_window(self):
        self.stop()
        self.btnLoadParameters['state'] = "disabled"
        
        self.load_parameters_window = tk.Toplevel()
        self.load_parameters_window.title("Charger des paramètres préenregistrés")
           
        
        # Création de tous les radio buttons pour sélectionner les pendule sur lequel on applique les paramètres préenregistrés
        self.pendulum_size_var = tk.DoubleVar()
        self.pendulum_size_var.set(self.l)
        self.pendulum_size_choice_frame = tk.Frame(self.load_parameters_window)
        tk.Label(self.load_parameters_window, text = "Pendule à utiliser :" ).pack()
        tk.Radiobutton(self.pendulum_size_choice_frame,text="2cm",variable=self.pendulum_size_var, value=2e-2).pack(side=tk.LEFT)
        tk.Radiobutton(self.pendulum_size_choice_frame,text="4cm",variable=self.pendulum_size_var, value=4e-2).pack(side=tk.LEFT)
        tk.Radiobutton(self.pendulum_size_choice_frame,text="6cm",variable=self.pendulum_size_var, value=6e-2).pack(side=tk.LEFT)
        tk.Radiobutton(self.pendulum_size_choice_frame,text="8cm",variable=self.pendulum_size_var, value=8e-2).pack(side=tk.LEFT)
        tk.Radiobutton(self.pendulum_size_choice_frame,text="10cm",variable=self.pendulum_size_var, value=10e-2).pack(side=tk.LEFT)
        self.pendulum_size_choice_frame.pack()
         
        
        # On crée tous les boutons correspondants aux propositions de paramètres pré-enregistrés
        self.settings_buttons = []
        for setting in predefined_settings:
            button = tk.Button(self.load_parameters_window, 
                  text=setting["text"], 
                  command=lambda parameters=setting["parameters"]: self.load_parameters(parameters)
                  , bg="#DEDEDE", cursor="hand2")
            self.settings_buttons.append(button)
            button.pack(ipadx=5, ipady=20, padx=10, pady=10)
    
    
        self.update_parameters_buttons()
        update_fonc = self.update_parameters_buttons
        self.pendulum_size_var.trace("w", update_fonc)
        
        
        self.load_parameters_window.protocol("WM_DELETE_WINDOW", self.close_load_parameters_window)

        # Lancer la boucle principale de la fenêtre
        self.load_parameters_window.mainloop()

    
    def close_load_parameters_window(self):
        self.btnLoadParameters['state'] = "normal"
        self.load_parameters_window.destroy()
        
    def update_parameters_buttons(self, *args, **kargs):
        """
            Actualise chaque dernière ligne de boutons de paramètre prédéfini 
            ui donne l'apperçu des paramètres qui vont être mis
        """
                 
        
        for k in range(len(self.settings_buttons)):
            button = self.settings_buttons[k]
            
            parameters = predefined_settings[k]["parameters"]
            evalued_parameters = self.eval_parameters(predefined_settings[k]["parameters"])
            
            button_text_splitted = button['text'].split("\n")
            
            parameters_indication = "("
            
            if parameters["thetadeb"] == "actuel" or isinstance(parameters["thetadeb"], str):
                parameters_indication+= "thetadeb="+parameters["thetadeb"]+"="+str(round(evalued_parameters["thetadeb"], 5))+"   ;   "
            else:
                parameters_indication+= "thetadeb="+str(round(evalued_parameters["thetadeb"], 5))+"   ;   "
            
            if parameters["alpha"] == "actuel" or isinstance(parameters["alpha"], str):
                parameters_indication+= " ="+parameters["alpha"]+"="+str(round(evalued_parameters["alpha"], 5))+"   ;   "
            else:
                parameters_indication+= "α="+str(round(evalued_parameters["alpha"], 5))+"   ;   "
            
            if parameters["f"] == "actuel" or isinstance(parameters["f"], str):
                parameters_indication+= "f="+parameters["f"]+"="+str(round(evalued_parameters["f"], 5))+"   ;   "
            else:
                parameters_indication+= "f="+str(round(evalued_parameters["f"], 5))+"   ;   "
                
            if parameters["a"] == "actuel" or isinstance(parameters["a"], str):
                parameters_indication+= "a="+parameters["a"]+"="+str(round(evalued_parameters["a"], 5))
            else:
                parameters_indication+= "a="+str(round(evalued_parameters["a"], 5))
            
            parameters_indication += ")"
            
            
            
            
            button['text'] = "\n".join(button_text_splitted[:-1])+"\n"+parameters_indication
        
        
        
    def eval_parameters(self, parameters):
        """
            Permet d'évaluer des paramètres thetadeb, alpha, f et a 
            lorsqu'il sont sous la forme d'un calcul dans une chaine de caractères
            utilisant f0.
        """
            
        # Si les valeurs valent "actuel", on considère qu'elles ne changent pas par rapport à avant.
        if parameters["thetadeb"] == "actuel":
            thetadeb = self.theta_scale.get()
        else:
            thetadeb = parameters["thetadeb"]
            
        if parameters["alpha"] == "actuel":
            alpha = self.alpha_var.get()
        else :
            alpha = parameters["alpha"]
            
        if parameters["f"] == "actuel":
            f = self.f_var.get()
        else:
            f = parameters["f"]
            
        if parameters["a"] == "actuel":
            a = self.a_var.get()
        else:
            a = parameters["a"]
            
        
        # si la valeur est de la forme d'une expression qui dépend de f0
        f0 = theory.calc_f0(self.pendulum_size_var.get(), self.g)
        
        if isinstance(thetadeb, str):
            thetadeb.replace('f0', str(f0))
            thetadeb = eval(thetadeb)
        if isinstance(alpha, str):
            alpha.replace('f0', str(f0))
            alpha = eval(alpha)
        if isinstance(f, str):
            f.replace('f0', str(f0))
            f = eval(f)
        if isinstance(a, str):
            a.replace('f0', str(f0))
            a = eval(a)
            
            
        return {"thetadeb":thetadeb, "alpha":alpha, "f":f, "a":a}

    def load_parameters(self, parameters):
        evalued_parameters = self.eval_parameters(parameters)
        
        self.l = self.pendulum_size_var.get()
        self.L = self.l*100/5 
        self.theta_scale.set(evalued_parameters["thetadeb"])
        self.alpha_var.set(evalued_parameters["alpha"])
        self.f_var.set(evalued_parameters["f"])
        self.a_var.set(evalued_parameters["a"])
        
        self.start()
        
        self.close_load_parameters_window()
        
    def open_graphics(self):
        # on regénère le modèle
        t, theta = theory.calc_pendule(
            thetadeb=self.theta_scale.get(),
            alpha=self.alpha_var.get(),
            f=float(self.f_var.get()),
            a=float(self.a_var.get()),
            l = float(self.l),
            g = float(self.g),
            tau = float(self.tau),
            tfin= self.tfin,
            output=["t", "theta"]
        ).values()
        
        # on l'affiche
        theory.plot_pendule_evolution(t, theta)
        print("\nGenerated graphic with parameters :\n",
              "{thetadeb=", str(round(self.theta_scale.get(), 5)),
              "; alpha =", str(round(self.alpha_var.get(), 5)),
              "; f =", str(round(float(self.f_var.get()), 5)),
              "; a =", str(round(float(self.a_var.get()), 5)),
              "; l =", str(round(float(self.l), 5)),
              "; g =", str(round(float(self.g), 5)),
              "; tau =", str(round(float(self.tau), 5)),
              "; tfin=", str(round(float(self.tfin), 5)), "}"
             )

    def open_simulation_graphics(self):

        t, theta, N = theory.calc_pendule(
            thetadeb=self.theta_scale.get(),
            alpha=self.alpha_var.get(),
            f=float(self.f_var.get()),
            a=float(self.a_var.get()),
            l = float(self.l),
            g = float(self.g),
            tau = float(self.tau),
            tfin= self.tfin,
            output=["t", "theta", "N"]
        ).values()
        
        # on l'affiche
        theory.plot_pendule_evolution(t[::int(N/self.N)], theta[::int(N/self.N)])
        print("\nGenerated graphic of really played by tkinter (less occurences) model with parameters :\n",
              "{thetadeb=", str(round(self.theta_scale.get(), 5)),
              "; alpha =", str(round(self.alpha_var.get(), 5)),
              "; f =", str(round(float(self.f_var.get()), 5)),
              "; a =", str(round(float(self.a_var.get()), 5)),
              "; l =", str(round(float(self.l), 5)),
              "; g =", str(round(float(self.g), 5)),
              "; tau =", str(round(float(self.tau), 5)),
              "; tfin=", str(round(float(self.tfin), 5)), "}"
             )


if __name__ == "__main__":
    simu_pendule = AppliPendule()
    simu_pendule.mainloop()
