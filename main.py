# -*- coding: utf-8 -*-

from utils import *
from ui import App, Tk

# show_ui = False
show_ui = True

if show_ui is True : 
    fenetre = Tk()
    app = App(fenetre)
    fenetre.mainloop()
    exit()


damier = creer_damier()
joueur = 1
fin = False

while (fin is False):
    affiche2(damier, joueur)
    
    couleur = "noir" if joueur == 1 else "blanc"
    estValide = False
    while (estValide is False):
        case = input("Joueur " + couleur + ", dans quelle case voulez-vous jouer ?")
        estValide = joue(damier, joueur, case)
        if (case == "q"):
            fin = True
            break

    joueur = 2 if joueur == 1 else 1
    

