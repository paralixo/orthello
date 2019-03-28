# -*- coding: utf-8 -*-

from tkinter import *
from utils import *

class App:
    fenetre = None
    canvas = None
    frame = None
    show_debug = True
    damier = []
    damier_ui = []
    longueur = 0
    hauteur = 0
    joueur = 1
    fin = False

    def __init__(self, fenetre):
        # UI
        self.fenetre = fenetre

        self.frame = Frame(self.fenetre, borderwidth = 2, relief = GROOVE)
        Label(self.frame, text = "Frame bison").pack(padx=10, pady=10)
        self.frame.pack(side=RIGHT)

        self.damier = creer_damier()
        self.longueur = len(self.damier[0])
        self.hauteur = len(self.damier)

        self.canvas = Canvas(fenetre, width = 360, height = 360, background = '#CD853F')
        
                
        # for i in range (self.hauteur):
        #     ligne = []
        #     for j in range (self.longueur):
        #         logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(0)) 
        #         img = self.canvas.create_image(i * 32 + 20, j * 32 + 20, image = logo)
        #         ligne.append(img)
        #     self.damier_ui.append(ligne)

        self.canvas.pack(side=LEFT)

        self.draw()

    def game(self):
        print('game')

    def draw(self):
        logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(0)) 
        img = self.canvas.create_image(40, 40, image = logo)
        if (self.show_debug is True) : affiche2(self.damier, self.joueur)

        for i in range(self.hauteur + 1):
            self.canvas.create_line(20, i * 32 + 20, self.longueur * 32 + 20,  i * 32 + 20)
        for j in range(self.longueur + 1):
            self.canvas.create_line(j * 32 + 20, 20,  j * 32 + 20, self.hauteur * 32 + 20)

        cpt = -1
        for i in range (self.hauteur):
            for j in range (self.longueur):
                cpt += 1

                if (self.damier[i][j] == 1):
                    logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(0)) 
                    img = self.canvas.create_image(i * 32 + 20, j * 32 + 20, image = logo)
                elif (self.damier[i][j] == 2):
                    logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(6)) 
                    img = self.canvas.create_image(i * 32 + 20, j * 32 + 20, image = logo)
                elif (estValide(self.damier, self.joueur, cpt) is True):
                    logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(3)) 
                    img = self.canvas.create_image(i * 32 + 20, j * 32 + 20, image = logo)
