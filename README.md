# Outils d'étude du comportement d'un pendule 
## Faire des calculs
Le fichier "pendule_euler.py" permet de calculer certaines valeurs pour un pendule donné en utilisant la méthode d'Euler.

### Fonctions :
### 1 - calc_pendule
Calcule l'évolution de l'angle d'un pendule soumis ou non à un excitation verticale ou  horizontale. Calcule également la fréquence propre du pendule donné et le renvoie si demandé en output.
exemple d'utilisation :
```python
    calc_pendule(l=5e-2, thetadeb=45, alpha=0, f=5, a=1e-2, g=9.81, tfin=10, output=["t", "theta", "thetap", "f0", "fmin"])
```
--> retourne un dictionnaire contenant, pour un pendule de longueur 5cm, à un angle de 45 degrès par rapport au bas, soumis à une excitation verticale de fréquence 5Hz et d'amplitude 1cm sur une durée de simulation de 10s :
- l'array numpy de temps
- l'array numpy des angles theta du pendule au cours du temps
- l'array numpy des vitesses angulaire thetap du pendule au cours du temps
- la fréquence propre du pendule (dépend de sa longueur l et de l'attraction terrestre g)
- la fréquence minimale du pendule


### 2 - calc_f0
Calcule seulement la fréquence propre f0 d'un pendule de longueur l soumis à une attraction terrestre g
exemple d'utilisation :
```python
    calc_f0(6e-2, 9.81)
```
--> renvoie la fréquence propre d'un pendule de longueur 6cm pour l'attraction terrestre normale
    
### 3 - plot_pendule_evolution
Permet de tracer l'evolution de l'angle du pendule par rapport à la verticale descendante
exemple d'utilisation :
```python

    t, theta = tuple(calc_pendule(l=5e-2, thetadeb=45, alpha=0, f=5, a=1e-2, g=9.81, tfin=10, output=["t", "theta"]).values())
    plot_pendule_evolution(t, theta)
    
```
--> trace le graphique mathplotlib de theta en fonction du temps pour les conditions énoncées précedement. Il est à noter que dans l'éditeur python Spider, le graphique s'affichera dans une rubrique dédiée alors que via tout autre moyen d'execution, le graphique apparaître dans une fenêtre séparée. A vous de voir l'affichage que vous préférez ! ;)


## Afficher
Le fichier "modélisation d'un pendule avec excitation.py" affiche une fenêtre tkinter permettant de visualiser graphiquement le mouvement d'un pendule soumis à diverses conditions, de tracer en un clic son graphique "theta en fonction de t" et d'obtenir facilement sa fréquence et sa période propre.
Des paramètre prédéfinis peuvent même être sélectionnés pour mettre en évidence les phénomènes que nous désirons étudier 🙂
De légers lags peuvent apparaître, mais ils sont normalement courts.

🕰️

## Galerie
![Graphique "theta en fonction de t" d'un pendule de longueur 5cm, à un angle de 45 degrès par rapport au bas, soumis à une excitation verticale de fréquence 5Hz et d'amplitude 2cm sur une durée de simulation de 10s](images/graphic%20example.png)

![Aperçu de l'outil](images/simulation%20playing.png)

![Utilisation de paramètres pré-enregistrés](images/pre-loaded%20parameters.png)

![Autres propriétés et obtention de la fréquence et de la période propres](images/other%20properties.png)
