from tkinter import *


class BarreDoutils(Menu):
    """Barre d'outils contenant les options de sauvegarde, chargement,
    etc"""


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
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss **kwargs) #toplevel est fenêtre popup
        self.geometry("300x300+10x10") #300x300 donne dimension, 10x10 donne
        self.resizable(width=0, height=0) #empeche resize
        Bouton(self, text="1 joueur", command="self.unjoueur").pack(pady=5, padx=10)
        Bouton(self, text="2 joueurs", command="self.deuxjoueurs").pack(pady=5, padx=10)

    def unjoueur(self):
        """ouvre une FenNiveauDif si 1 joueur choisi"""
        self.fen1 = FenNiveauDif(self)

    def deuxjoueurs(self):
        """ouvre FenTypePartie si 2 joueurs"""
        self.fen1 = FenNiveauDif(self)


class FenNiveauDif(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le niveau de
    difficulté des parties à 1 joueur.
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss, **kwargs)
        self.geometry("300x300+10x10")
        self.resizable(width=0, height=0)
        Bouton(self, text="Normal", command="").pack(pady=5, padx=10)
        Bouton(self, text="Difficile", command="").pack(pady=5, padx=10)
        Bouton(self, text="Légendaire", command="").pack(pady=5, padx=10)


class FenTypePartie(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le type de partie
    soit classique ou personnalisée
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss, **kwargs)
        self.geometry("300x300+10x10")
        self.resizable(width=0, height=0)
        Glissoir(self, )
        Bouton(self, text="Jouer!", command="").pack(pady=5, padx=10)


class FenPartiePerso(Toplevel):
    """
    Fenêtre satellite contenant les options de personnalisations lorsque le
    joueur choisi de faire une partie personnalisée
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss, **kwargs)
        self.geometry("500x500+10x10")


class Application(object):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        self.root =Tk()
        self.root.title('Othello avec un nom plus cool')


