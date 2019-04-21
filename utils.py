# -*- coding: utf-8 -*-

import re

# Création du damier par rapport à la longueur/largeur souhaité
# longueur et largeur -> int
def creer_damier(hauteur = 6, longueur = 6):
    if (longueur%2 != 0 or hauteur%2 != 0):
        print("Erreur damier init")
        return 1

    damier = []

    for i in range (hauteur):
        ligne = []
        for j in range (longueur):
            ligne.append(0)
        damier.append(ligne)

    demi_longueur = int(longueur/2)
    demi_hauteur = int(hauteur/2)
    damier[demi_hauteur-1][demi_longueur-1]=2
    damier[demi_hauteur][demi_longueur]=2
    damier[demi_hauteur-1][demi_longueur]=1
    damier[demi_hauteur][demi_longueur-1]=1

    return damier

# Affiche le numéro de la ligne courante 
# i -> ligne courante -> int
def affiche_num_ligne(i):
    print(str(i) + (' ' if i < 10 else ''), end = '')

# Affiche tout les numéros de colonne du damier
# longueur -> len(damier[0]) -> int
def affiche_num_colonne(longueur):
    print('   ', end = '')
    for k in range(longueur):
        print(str(k) + (' ' if k < 10 else ''), end = '')
    print()

# Affichage du damier
# damier -> liste de liste d'entiers
def affiche(damier):
    longueur = len(damier[0])
    hauteur = len(damier)

    print()
    for i in range (hauteur):
        affiche_num_ligne(i)
        for j in range (longueur):
            print('|', end = '')

            value = ' '
            if (damier[i][j] == 1):
                value = 'X'
            elif (damier[i][j] == 2):
                value = 'O'
            print(value, end = '')

            if (j == longueur - 1):
                print('|', end = '')
        print()
    affiche_num_colonne(longueur)

# Affichage du damier
# + affichage des cases jouables pour le joueur
def affiche2(damier, joueur):
    longueur = len(damier[0])
    hauteur = len(damier)
    case = 0
    jeuFini = True
    peutJouer = False

    print()
    for i in range (hauteur):
        affiche_num_ligne(i)
        for j in range (longueur):
            case = str(i) + str(j)
            print('|', end = '')

            value = ' '
            if (damier[i][j] == 1):
                value = 'X'
            elif (damier[i][j] == 2):
                value = 'O'
            elif (estValide(damier, joueur, case) is True):
                value = '.'
                jeuFini = False
                peutJouer = True
            else:
                jeuFini = False
            print(value, end = '')

            if (j == longueur - 1):
                print('|', end = '')
        print()
    affiche_num_colonne(longueur)

    return (jeuFini, peutJouer)

# Retourne la ligne et la colonne pour un numéro de case donnée
# damier -> liste de liste d'entiers
# case -> entier
def lignecolonne(case):
    rslt = (0, 0)

    if (case < 10):
        rslt = (0, case)
    else:
        i = int(str(case)[0])
        j = int(case % 10)
        rslt = (i, j)

    return rslt

# teste la direction (delta_i, delta_j) ((int, int) -> compris entre -1 et 1 (0,0) non possible)) par rapport à la case choisi et le joueur 
# retourne True si la case est jouable au sense orthello du terme (partie de estValide())
def testdirection(damier, joueur, case, delta_i, delta_j, est_dispo = False):
    estValide = False
    longueur = len(damier[0])
    hauteur = len(damier)
    i, j = lignecolonne(case)
    ennemi = 2 if joueur == 1 else 1
    ennemiPresent = False
    
    fin = False
    if (est_dispo is True and damier[i][j] != 0):
        fin = True
    while (fin is False):
        i, j = i + delta_i, j + delta_j
        if (j < 0 or j >= longueur or i < 0 or i >= hauteur):
            fin = True
            break
        if (damier[i][j] == 0):
            fin = True
        elif (damier[i][j] == ennemi):
            ennemiPresent = True
        elif (damier[i][j] == joueur and ennemiPresent is True):
            estValide = True
            fin = True
        elif (damier[i][j] == joueur and ennemiPresent is False):
            estValide = False
            fin = True

    return estValide

# retourne True si la case est jouable au sense orthello du terme
def estValide(damier, joueur, case):
    if (type(case) != int):
        if (re.match(r"^\d+$", case) is None):
            return False
        case = int(case)

    # if (case > (hauteur * longueur) - 1 or case < 0):
    if (case < 0):
        return False

    estValide = False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 or j != 0):
                estValide = testdirection(damier, joueur, case, i, j, est_dispo=True)
            if (estValide is True): break
        if (estValide is True): break
    
    return estValide

def consequences(damier, joueur, case):
    case = int(case)
    directions = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 or j != 0):
                if(testdirection(damier, joueur, case, i, j) is True):
                    directions.append((i, j))

    ennemi = 2 if joueur == 1 else 1
    for dir in directions:
        i, j = lignecolonne(case)
        fin = False
        while (fin is False):
            i, j = i + dir[0], j + dir[1]
            if (damier[i][j] == joueur):
                fin = True
            if (damier[i][j] == ennemi):
                damier[i][j] = joueur

# Vérifie qu'on peut jouer dans la case choisie
# damier -> liste de liste d'entiers
# joueur -> entier
# case -> entrée utilisateur (censé être un entier)
def joue(damier, joueur, case):
    if (estValide(damier, joueur, case) is True):
        i, j = lignecolonne(int(case))
        damier[i][j] = joueur
        consequences(damier, joueur, case)
        return True
    else:
        print("Case impossible, ", end = '')
        return False

def score(damier):
    score_j1 = 0
    score_j2 = 0
    longueur = len(damier[0])
    hauteur = len(damier)

    for i in range (hauteur):
        for j in range (longueur):
            if (damier[i][j] == 1):
                score_j1 += 1
            elif (damier[i][j] == 2):
                score_j2 += 1

    return score_j1, score_j2