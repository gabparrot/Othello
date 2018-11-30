from tkinter import *
from othello.exceptions import ErreurPositionCoup
from othello.partie import Partie

# TODO convertir la position demandée sur le GUI Format (A, 1) en format (0, 0)
# TODO avant de la valider ou de la jouer

# TODO À chaque coup demandé, verifier avec self.partie.exceptions


# === Définition des objets esclaves et de leurs éléments de style === #

# class BarreDoutils(MenuButton):
#     """Barre d'outils contenant les options de sauvegarde, chargement,
#     etc"""


class Bouton(Button):
    """Classe définissant le style des boutons utilisés dans le jeu"""
    def __init__(self, boss, **kwargs):
        Button.__init__(self, boss, bg="dark grey", fg="brown", bd=5,
                        activebackground="blue", activeforeground="brown",
                        font='Helvetica', **kwargs)


class Glissoir(Scale):
    """Classe définissant le style des glissoirs gradués"""
    def __init__(self, boss, **kwargs):
        Scale.__init__(self, boss, **kwargs)


class PlancheDeJeu(Canvas):
    """le damier"""
    def __init__(self, boss):
        Canvas.__init__(self, boss, width=500, height=500, bg='ivory')

class FenJoueurs(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss **kwargs)  # toplevel est fenêtre popup
        self.geometry("300x300+10x10")  # 300x300 donne dimension, 10x10 donne
        self.resizable(width=0, height=0)  # empeche resize
        Bouton(self, text="1 joueur", command=self.unjoueur).pack(pady=5, padx=10)
        Bouton(self, text="2 joueurs", command=self.deuxjoueurs).pack(pady=5, padx=10)

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


class Historique(Frame):
    """Défini la zone de texte avec l'historique des coups joués"""
    def __init__(self, boss, width=25, height=25):
        Frame.__init__(self, boss, bd=2, bg='white',
                       width=width, height=height, relief=SUNKEN)
        self.text = Text(self, font='Helvetica', bg='white', bd=1, width=width,
                         height=height)
        scroll = Scrollbar(self, bd=1, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        scroll.pack(side=RIGHT, expand=NO, fill=X, padx=2, pady=2)

    def ajouter_texte(self, action_a_ecrire):
        self.text.insert(END, action_a_ecrire)


class ScoreActuel(Label):
    def __init__(self, boss):
        Label.__init__(self, boss, font='Helvetica', text="score: ")

    def changer_score(self, score_a_ecrire):
        self.labelText =('1.0', score_a_ecrire)


    # ====== Object maître / fenêtre principale  ====== #

class Application(Tk):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        Tk.__init__(self)  # Constructeur de la classe maître
        self.partie = Partie()
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=1, column=0, rowspan=3)
        self.title("Nom qu'on donnera au jeu")
        self.barre_menu = Menubutton
        # TODO servira à afficher coups possibles ou si trop dur à jouer un
        # TODO coup possible au hasard à la place du joueur
        Bouton(self, text="Voir les coups possibles",
                              command=None).grid(row=0, column=0, padx=5,
                                                 pady=5, sticky=W)
        Bouton(self, text="Nouvelle partie",
                                      command=None).grid(row=1, column=2,
                                                         padx=5, pady=5)
        Bouton(self, text="Abandonner", command=None)\
            .grid(row=2, column=2, padx=5, pady=5)
        Historique(self).grid(row=3, column=2)
        ScoreActuel(self).grid(row=4, column=2)


# ====== Exécution du programme principal ====== #

le_jeu = Application()
le_jeu.mainloop()
