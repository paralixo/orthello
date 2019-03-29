# -*- coding: utf-8 -*-

from tkinter import *
from utils import *
from math import trunc as truncate

class App:
    fenetre = None
    canvas = None
    frame = None
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

    def __init__(self, fenetre):
        # Logique
        self.damier = creer_damier()
        self.longueur = len(self.damier[0])
        self.hauteur = len(self.damier)

        # UI
        self.fenetre = fenetre
        self.frame = Frame(self.fenetre, borderwidth = 2, relief = GROOVE)
        Label(self.frame, text = "Frame bison").pack(padx=10, pady=10)
        self.frame.pack(side=RIGHT)

        self.canvas = Canvas(fenetre, width = 360, height = 360, background = '#CD853F')
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.pack(side=LEFT)

        # Charger les images dans une liste 
        for i in range(self.nombre_sprites):
            self.img_pions.append(PhotoImage(file=self.file_img_pions, format="gif -index " + str(i)))

        self.affiche()

    def clic(self, event):
        x, y = event.x, event.y
        if (self.show_debug is True) : print("Clic détecté (" + str(x) + ", " + str(y) +")")
        
        if (x > 20 and y > 20 and x < self.longueur * self.cote_image + self.padding and y < self.hauteur * self.cote_image + self.padding):
            x = truncate((x-20)/32)
            y = truncate((y-20)/32)
            case = str(y) + str(x)
            if (self.show_debug is True) : print("Case = " + case)
            joue(self.damier, self.joueur, case)
            self.joueur = 2 if self.joueur == 1 else 1

            self.canvas.delete("all")
            self.affiche()

    def affiche_plateau(self, padding, c_img):
        for i in range(self.hauteur + 1):
            self.canvas.create_line(padding, i * c_img + padding, self.longueur * c_img + padding, i * c_img + padding)
        for j in range(self.longueur + 1):
            self.canvas.create_line(j * c_img + padding, padding, j * c_img + padding, self.hauteur * c_img + padding)

    def affiche_jeu(self, padding, c_img):
        img_padding = c_img/2 + padding
        for i in range (self.hauteur):
            for j in range (self.longueur):
                case = str(j) + str(i)
                if (self.damier[j][i] == 1):
                    self.canvas.create_image(i * c_img + img_padding, j * c_img + img_padding, image = self.img_pions[0])
                elif (self.damier[j][i] == 2):
                    self.canvas.create_image(i * c_img + img_padding, j * c_img + img_padding, image = self.img_pions[6])
                elif (estValide(self.damier, self.joueur, case) is True):
                    self.affiche_croix(padding, c_img, i, j)

    def affiche_croix(self, padding, c_img, i, j):
        self.canvas.create_line(i * c_img + padding, j * c_img + padding, (i+1) * c_img + padding, (j+1) * c_img + padding)
        self.canvas.create_line((i+1) * c_img + padding, j * c_img + padding, i * c_img + padding, (j+1) * c_img + padding)

    def affiche(self):
        if (self.show_debug is True) : affiche2(self.damier, self.joueur)
        self.affiche_plateau(self.padding, self.cote_image)
        self.affiche_jeu(self.padding, self.cote_image)
        
