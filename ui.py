# -*- coding: utf-8 -*-

from tkinter import *
from utils import *

class App:
    fenetre = None
    canvas = None
    frame = None
    img_pions = []

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
        self.canvas.pack(side=LEFT)

        # Charger les images dans une liste 
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 0"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 1"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 2"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 3"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 4"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 5"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 6"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 7"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 8"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 9"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 10"))
        self.img_pions.append(PhotoImage(file='assets/orthello_animation.gif', format="gif -index 11"))

        self.affiche()

    def affiche(self):
        if (self.show_debug is True) : affiche2(self.damier, self.joueur)

        padding = 20
        c_img = 32

        # draw damier
        for i in range(self.hauteur + 1):
            self.canvas.create_line(padding, i * c_img + padding, self.longueur * c_img + padding,  i * c_img + padding)
        for j in range(self.longueur + 1):
            self.canvas.create_line(j * c_img + padding, padding,  j * c_img + padding, self.hauteur * c_img + padding)

        # draw pieces
        for i in range (self.hauteur):
            for j in range (self.longueur):
                if (self.damier[i][j] == 1):
                    self.canvas.create_image(i * c_img + (c_img/2 + padding), j * c_img + (c_img/2 + padding), image = self.img_pions[0])
                elif (self.damier[i][j] == 2):
                    self.canvas.create_image(i * c_img + (c_img/2 + padding), j * c_img + (c_img/2 + padding), image = self.img_pions[6])
        
