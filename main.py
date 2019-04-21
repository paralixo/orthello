# -*- coding: utf-8 -*-

from utils import *
from ui import App, Tk

show_ui = True

if show_ui is True : 
    fenetre = Tk()
    app = App(fenetre)
    fenetre.mainloop()
    exit()


damier = creer_damier()
joueur = 1
fin = False
score_j1 = 0
score_j2 = 0

while (fin is False):
    fin, peutJouer = affiche2(damier, joueur)
    
    couleur = "noir" if joueur == 1 else "blanc"

    if (peutJouer is True):
        estValide = False
        while (estValide is False):
            case = input("Joueur " + couleur + ", dans quelle case voulez-vous jouer ?")
            estValide = joue(damier, joueur, case)
            if (case == "q"):
                fin = True
                break

        score_j1, score_j2 = score(damier)
        print("scorej1 = " + str(score_j1) + "; scorej2 = " + str(score_j2))
    
    joueur = 2 if joueur == 1 else 1
    

