from utils import *

damier = creer_damier()

damier[4][4]=2
damier[5][5]=2
damier[4][5]=1
damier[5][4]=1
damier[0][0]=1
damier[0][1]=2
damier[0][2]=2
damier[8][5]=1
damier[7][6]=2
damier[6][7]=2
damier[7][5]=1
damier[5][7]=1

joueur = 1
fin = False

while (fin is False):
    # affiche(damier)
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
    