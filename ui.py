# -*- coding: utf-8 -*-

from tkinter import *
from utils import *
from math import trunc as truncate
import random
import time

class App:
    fenetre = None
    canvas = None
    frame = None
    choix_j1 = None
    choix_j2 = None
    bouton = None
    l_score_j1 = None
    l_score_j2 = None
    l_joueur = None
    img_pions = []
    file_img_pions = "assets/orthello_animation.gif"
    padding = 20
    cote_image = 32
    nombre_sprites = 12

    show_debug = True

    damier = []
    longueur = 0
    hauteur = 0
    joueur = 1
    fin = False
    peutJouer = True
    score_j1 = 0
    score_j2 = 0

    def __init__(self, fenetre):
        # Logique
        self.damier = creer_damier()
        self.longueur = len(self.damier[0])
        self.hauteur = len(self.damier)

        # UI
        self.fenetre = fenetre
        self.frame = Frame(self.fenetre, borderwidth = 2, relief = GROOVE)

        self.choix_j1 = StringVar(self.frame)
        self.choix_j1.set("humain")
        self.choix_j2 = StringVar(self.frame)
        self.choix_j2.set("humain")
        self.j1 = OptionMenu(self.frame, self.choix_j1, "humain", "ordi")
        self.j1.pack()
        self.j2 = OptionMenu(self.frame, self.choix_j2, "humain", "ordi")
        self.j2.pack()
        self.bouton = Button(self.frame, text="Lancer partie", command=self.commencer)
        self.bouton.pack()

        self.l_score_j1 = Label(self.frame, text = 'Score J1 (noir) = 2')
        self.l_score_j1.pack()
        self.l_score_j2 = Label(self.frame, text = 'Score J2 (blanc) = 2')
        self.l_score_j2.pack()
        self.l_joueur = Label(self.frame, text = 'Joueur : noir')
        self.l_joueur.pack()

        self.frame.pack(side=RIGHT)

        self.canvas = Canvas(fenetre, width = 360, height = 360, background = '#CD853F')
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.pack(side=LEFT)

        # Charger les images dans une liste 
        for i in range(self.nombre_sprites):
            self.img_pions.append(PhotoImage(file=self.file_img_pions, format="gif -index " + str(i)))

        self.affiche()

    def commencer(self):
        self.damier = creer_damier()
        self.longueur = len(self.damier[0])
        self.hauteur = len(self.damier)
        self.score_j1, self.score_j2 = score(self.damier)
        self.l_score_j1.configure(text = 'Score J1 (noir) = {}'.format(self.score_j1))
        self.l_score_j2.configure(text = 'Score J2 (blanc) = {}'.format(self.score_j2))
        print(self.choix_j1.get())
        self.canvas.delete("all")
        self.affiche()

    # Gestion du clic
    def clic(self, event):
        # On récupère les coordonnées du clic
        x, y = event.x, event.y
        if (self.show_debug is True) : print("Clic détecté (" + str(x) + ", " + str(y) +")")
        
        # Eviter que de jouer pendant le tour de l'ordi
        choix = self.choix_j1 if self.joueur == 1 else self.choix_j2
        if (choix.get() != "humain"):
            return None

        # On vérifie qu'on clique bien dans les limites du plateau de jeu puis on trouve de quelle case il s'agit
        if (x > self.padding and y > self.padding and x < self.longueur * self.cote_image + self.padding and y < self.hauteur * self.cote_image + self.padding):
            x = truncate((x-self.padding)/32)
            y = truncate((y-self.padding)/32)
            case = str(y) + str(x)
            if (self.show_debug is True) : print("Case = " + case)

            # Si possible, on joue puis on recalcule les scores et on passe au joueur suivant
            if (self.peutJouer is True):
                estValide = joue(self.damier, self.joueur, case)
                if (estValide is True) :
                    self.score_j1, self.score_j2 = score(self.damier)
                    self.l_score_j1.configure(text = 'Score J1 (noir) = {}'.format(self.score_j1))
                    self.l_score_j2.configure(text = 'Score J2 (blanc) = {}'.format(self.score_j2))
                    self.joueur = 2 if self.joueur == 1 else 1
                    self.l_joueur.configure(text = "Joueur " + ("noir" if self.joueur == 1 else "blanc"))

            # On efface le contenu du canvas et on réaffiche
            self.canvas.delete("all")
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

    def affiche(self):
        if (self.show_debug is True) : affiche2(self.damier, self.joueur)

        # Affichage "pur" + récupération de variables
        self.affiche_plateau(self.padding, self.cote_image)
        self.fin, self.peutJouer, cases_jouables = self.affiche_jeu(self.padding, self.cote_image)

        # Si on ne peut pas jouer on change de joueur
        if (self.peutJouer is False and self.fin is False): 
            self.joueur = 2 if self.joueur == 1 else 1
            self.l_joueur.configure(text = "Joueur " + ("noir" if self.joueur == 1 else "blanc"))
            self.fin, self.peutJouer, cases_jouables = self.affiche_jeu(self.padding, self.cote_image)

            # Si le joueur suivant ne peut toujours pas jouer : égalité
            if (self.peutJouer is False): 
                print("Egalité !")
                self.fin = True 

        # Fin de la partie
        if (self.fin is True):
            print("Fin !")

        # Tour de l'ordi
        choix = self.choix_j1 if self.joueur == 1 else self.choix_j2
        if (choix.get() != "humain"):
            print("L'ordi joue mtn")
            #possibilites = []
            #for case in cases_jouables:
            #    damier_test = list(self.damier)
            #    scoree = consequences(damier_test, self.joueur, case)
            #    damier_test = []
            #    possibilites.append((case, scoree))
            #print(possibilites)

            joue(self.damier, self.joueur, random.choice(cases_jouables))
            
            self.score_j1, self.score_j2 = score(self.damier)
            self.l_score_j1.configure(text = 'Score J1 (noir) = {}'.format(self.score_j1))
            self.l_score_j2.configure(text = 'Score J2 (blanc) = {}'.format(self.score_j2))
            self.joueur = 2 if self.joueur == 1 else 1
            self.l_joueur.configure(text = "Joueur " + ("noir" if self.joueur == 1 else "blanc"))
            self.canvas.delete("all")
            self.affiche()
            time.sleep(1)
            
 