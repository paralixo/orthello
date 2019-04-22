# -*- coding: utf-8 -*-

from tkinter import *
from utils import *
from math import trunc as truncate
import copy

class App:
    # UI
    fenetre = None
    canvas = None
    choix_j1 = None
    choix_j2 = None
    l_score_j1 = None
    l_score_j2 = None
    l_joueur = None
    input = None
    img_pions = []
    file_img_pions = "assets/orthello_animation.gif"
    padding = 20
    cote_image = 32
    nombre_sprites = 12

    # Logique
    damier = []
    longueur = 0
    hauteur = 0
    joueur = 1
    fin = False
    peutJouer = True
    score_j1 = 0
    score_j2 = 0

    show_debug = True

    # Construction de l'application
    def __init__(self, fenetre):
        # UI
        self.fenetre = fenetre
        self.fenetre.title("Othello ~ Noé Baranes")
        self.fenetre.iconbitmap("assets/icon.ico")
        frame = Frame(self.fenetre, borderwidth = 2, relief = GROOVE)

        self.l_joueur = Label(frame, text = 'Tour Joueur : noir')
        self.l_joueur.pack()

        parametres = LabelFrame(frame, text = "Parametres :")
        self.choix_j1 = StringVar(parametres)
        self.choix_j1.set("humain")
        self.choix_j2 = StringVar(parametres)
        self.choix_j2.set("humain")
        OptionMenu(parametres, self.choix_j1, "humain", "ordi").grid(row=1, column=1)
        Label(parametres, text = "VS").grid(row=1, column=2)
        OptionMenu(parametres, self.choix_j2, "humain", "ordi").grid(row=1, column=3)
        Button(parametres, text="Relancer partie", command=self.commencer).grid(row=2, column=2)
        parametres.pack()
        
        score = LabelFrame(frame, text = "Scores : ")
        self.l_score_j1 = Label(score, text = 'Score J1 (noir) = 2')
        self.l_score_j1.pack()
        self.l_score_j2 = Label(score, text = 'Score J2 (blanc) = 2')
        self.l_score_j2.pack()
        score.pack()

        Label(frame, text = "Entrée manuelle : ").pack()
        self.input = Entry(frame, bd = 5)
        self.input.pack(side=LEFT)
        Button(frame, text="Valider", command=lambda:self.clic(type(Event), True)).pack(side=RIGHT)
        frame.pack(side=RIGHT)
        
        self.canvas = Canvas(fenetre, width = 232, height = 232, background = '#CD853F')
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.pack(side=LEFT)

        # Charger les images dans une liste 
        for i in range(self.nombre_sprites):
            self.img_pions.append(PhotoImage(file=self.file_img_pions, format="gif -index " + str(i)))

        self.commencer()

    # Mettre les parametres par defaut en (re)initialisant le damier
    def commencer(self):
        self.damier = creer_damier()
        self.longueur = len(self.damier[0])
        self.hauteur = len(self.damier)
        self.update_score()
        self.joueur = 1
        self.l_joueur.configure(text = "Tour Joueur " + ("noir" if self.joueur == 1 else "blanc"))
        self.affiche()

    # Gestion du clic / Tour du joueur
    def clic(self, event, manuelle = False):
        # Eviter que de jouer pendant le tour de l'ordi
        choix = self.choix_j1 if self.joueur == 1 else self.choix_j2
        if (choix.get() != "humain"):
            return None

        # On récupère les coordonnées du clic
        x, y = 0, 0
        if (manuelle is False):
            x, y = event.x, event.y
            if (self.show_debug is True) : print("Clic détecté (" + str(x) + ", " + str(y) +")")

        # On vérifie qu'on clique bien dans les limites du plateau de jeu puis on trouve de quelle case il s'agit
        if ((x > self.padding and y > self.padding and x < self.longueur * self.cote_image + self.padding and y < self.hauteur * self.cote_image + self.padding) or manuelle is True):
            if (manuelle is False):
                x = truncate((x-self.padding)/32)
                y = truncate((y-self.padding)/32)
                case = str(y) + str(x)
            else:
                case = self.input.get()         
            if (self.show_debug is True) : print("Case = " + case)

            # Si possible, on joue puis on recalcule les scores et on passe au joueur suivant
            if (self.peutJouer is True):
                estValide = joue(self.damier, self.joueur, case)
                if (estValide is True) :
                    self.apres_coup()

            self.affiche()

    # Affichage du quadrillage
    def affiche_plateau(self, padding, c_img):
        for i in range(self.hauteur + 1):
            self.canvas.create_line(padding, i * c_img + padding, self.longueur * c_img + padding, i * c_img + padding)
        for j in range(self.longueur + 1):
            self.canvas.create_line(j * c_img + padding, padding, j * c_img + padding, self.hauteur * c_img + padding)

    # Affichage des pions et cases jouables
    def affiche_jeu(self, padding, c_img):
        img_padding = c_img/2 + padding
        jeuFini = True
        peutJouer = False
        cases_jouables = []

        for i in range (self.hauteur):
            for j in range (self.longueur):
                case = str(j) + str(i)
                if (self.damier[j][i] == 1):
                    self.canvas.create_image(i * c_img + img_padding, j * c_img + img_padding, image = self.img_pions[0])
                elif (self.damier[j][i] == 2):
                    self.canvas.create_image(i * c_img + img_padding, j * c_img + img_padding, image = self.img_pions[6])
                elif (estValide(self.damier, self.joueur, case) is True):
                    cases_jouables.append(case)
                    self.affiche_croix(padding, c_img, i, j)
                    jeuFini = False
                    peutJouer = True
                else:
                    jeuFini = False

        return (jeuFini, peutJouer, cases_jouables)

    # Affiche une croix (utilisé pour représenter les cases jouables)
    def affiche_croix(self, padding, c_img, i, j):
        self.canvas.create_line(i * c_img + padding, j * c_img + padding, (i+1) * c_img + padding, (j+1) * c_img + padding)
        self.canvas.create_line((i+1) * c_img + padding, j * c_img + padding, i * c_img + padding, (j+1) * c_img + padding)

    # Lance l'affiche et gere la fin de la partie
    def affiche(self):
        if (self.show_debug is True) : affiche2(self.damier, self.joueur)

        # Affichage "pur" + récupération de variables
        self.canvas.delete("all")
        self.affiche_plateau(self.padding, self.cote_image)
        self.fin, self.peutJouer, cases_jouables = self.affiche_jeu(self.padding, self.cote_image)

        # Si on ne peut pas jouer on change de joueur
        if (self.peutJouer is False and self.fin is False): 
            self.joueur = 2 if self.joueur == 1 else 1
            self.l_joueur.configure(text = "Joueur " + ("noir" if self.joueur == 1 else "blanc"))
            self.fin, self.peutJouer, cases_jouables = self.affiche_jeu(self.padding, self.cote_image)

            # Si le joueur suivant ne peut toujours pas jouer : fin de la partie
            if (self.peutJouer is False): 
                print("Personne ne peut jouer !")
                self.fin = True 

        # Fin de la partie
        if (self.fin is True):
            j1, j2 = score(self.damier)
            if (j1 != j2):
                gagnant = "noir" if j1 > j2 else "blanc"
                score_gagnant = str(j1 if j1 > j2 else j2)
                score_perdant = str(j2 if j1 > j2 else j1)
                print("Fin ! Le joueur " + gagnant + " a gagné avec " + score_gagnant + " pions contre " + score_perdant)
            else:
                print("Egalité à " + str(j1) + " !")

        # Tour de l'ordi
        if (self.fin is False):
            choix = self.choix_j1 if self.joueur == 1 else self.choix_j2
            if (choix.get() != "humain"):
                if (self.show_debug is True) : print("Tour ordi (J" + str(self.joueur) + ")")
                self.canvas.update()
                self.canvas.after(2500, self.bot(cases_jouables))

    def bot(self, cases_jouables):
        # On récupère le nombre de pions retournés pour chacunes des cases jouables
        possibilites = []
        for case in cases_jouables:
            scoree = consequences(copy.deepcopy(self.damier), self.joueur, case)
            possibilites.append((case, scoree))

        # On choisit la case qui retourne le plus de pions en prenant en compte le positionnement de la case (coins, murs, ...)
        best_score = 0
        case_choisi = None
        for (case, score_possible) in possibilites:
            if (case == 0 or case == 50 or case == 5 or case == 55):
                score_possible += 10
            if (score_possible > best_score):
                best_score = score_possible
                case_choisi = case

        case = case_choisi
        if (self.show_debug is True) : print("Possibilités ('case', pions) : ", end = '')
        if (self.show_debug is True) : print(possibilites)
        if (self.show_debug is True) : print("Choix final : " + case)
        joue(self.damier, self.joueur, case)
        self.apres_coup()
        self.affiche()

    def apres_coup(self):
        self.update_score()
        self.joueur = 2 if self.joueur == 1 else 1
        self.l_joueur.configure(text = "Tour Joueur " + ("noir" if self.joueur == 1 else "blanc"))

    def update_score(self):
        self.score_j1, self.score_j2 = score(self.damier)
        self.l_score_j1.configure(text = 'Score J1 (noir) = {}'.format(self.score_j1))
        self.l_score_j2.configure(text = 'Score J2 (blanc) = {}'.format(self.score_j2))
        
 