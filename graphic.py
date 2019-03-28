# -*- coding: utf-8 -*-

from tkinter import *

fenetre = Tk()

label = Label(fenetre, text = "Hello world !")
label.pack()

canvas = Canvas(fenetre, width = 150, height = 120, background = 'yellow')
ligne1 = canvas.create_line(75, 0, 75, 120)
ligne2 = canvas.create_line(0, 60, 150, 60)
logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(6)) 

img = canvas.create_image(10, 10, image = logo)
txt = canvas.create_text(75, 60, text = "Cible", font = "Arial 16 italic", fill = "blue")
canvas.pack()


logo = PhotoImage(file='assets/orthello_animation.gif', format="gif - {}".format(1)) 
canvas.itemconfig(img, image = logo)

fenetre.mainloop()
