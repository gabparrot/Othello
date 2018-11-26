# UI de base va ici

from tkinter import *

class Bouton(Button):
    """Classe définissant le style des boutons utilisés dans le jeu"""
    def __init__(self, boss, **kwargs):
        Button.__init__(self, boss, bg="dark grey", fg="brown", bd=5,
                        activebackground="blue", activeforeground="brown",
                        font='Helvetica, 12, bold', **kwargs)

class Glissoir(Scale):
    """Classe définissant le style des glissoirs gradués"""
    def __init__(self, boss, **kwargs):
        Scale.__init__(self, boss, **kwargs)

class FenJoueurs(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """
    def __init__(self, **kwargs):
        Toplevel.__init__(self, **kwargs) #toplevel est fenêtre popup
        self.geometry("300x300+10x10") #300x300 donne dimension, 10x10 donne
        self.resizable(width=0, height=0) #empeche resize


class Application(object):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        self.root =Tk()
        self.root.title('Othello avec un nom plus cool')
