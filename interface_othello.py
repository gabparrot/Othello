from tkinter import *
from othello.exceptions import ErreurPositionCoup
from othello.partie import Partie
from sys import executable, argv
from os import execl
from tkinter import colorchooser

global difficulte
difficulte = "Normale"  # laisser le bug là m'tente pas d'enlever le global

# TODO convertir la position demandée sur le GUI Format (A, 1) en format (0, 0)
# TODO avant de la valider ou de la jouer

# TODO À chaque coup demandé, verifier avec self.partie.exceptions


# === Définition des objets esclaves et de leurs éléments de style === #
# class BarreDoutils(MenuButton):
#     """Barre d'outils contenant les options de sauvegarde, chargement,
#     etc"""
#     def __init__(self, boss, **kwargs):
#         Menubutton.__init__(self, boss, **kwargs)

class Color:
    color = "black"

    def choisir_couleur(self):
        clr = colorchooser.askcolor(title="Sélectionnez la couleur de votre choix")
        self.color = clr[1]

    def afficher_couleur(self):
        return str(self.color)

couleur = Color()

class Bouton(Button):
    """Classe définissant le style des boutons utilisés dans le jeu"""
    def __init__(self, boss, **kwargs):

        Button.__init__(self, boss, bg="dark grey", fg=couleur.afficher_couleur(), bd=5,
                        activebackground="grey", activeforeground="black",
                        font='Helvetica', **kwargs)


class Glissoir(Scale):
    """Classe définissant le style des glissoirs gradués"""
    def __init__(self, boss, **kwargs):
        Scale.__init__(self, boss, **kwargs)


class PlancheDeJeu(Canvas):
    """
    le damier, n'accepte présentement que des nombres pair de largeur de
    carrées, ex largeur de 6, 8, 10, 12 carrées de large
    """




    def __init__(self, boss, nb_cases=8):
        Canvas.__init__(self, boss, width=500, height=500, bg='ivory')
        self.larg = 500 // nb_cases
        self.nb_cases = nb_cases
        self.dessiner_carres(self.larg)
        self.centre_cases = self.trouver_centres(self.larg)


    def trouver_centres(self, larg):
        #TODO pas fini, fait juste 1 rangée
        centres = []
        for carre in range(1, self.nb_cases+1):
            centre_carre = larg * carre
            centres.append(centre_carre)
        return centres

    def dessiner_carres(self, larg):



        x, y = 1, 1
        for i in range(1, self.nb_cases + 1):
            if i % 2 != 0:
                for j in range(self.nb_cases//2):
                    self.create_rectangle(x, y, x + larg, y + larg,
                                          fill=couleur.afficher_couleur())
                    x += larg
                    self.create_rectangle(x, y, x + larg, y + larg,
                                          fill="white")
                    x += larg
            else:
                for j in range(self.nb_cases//2):
                    self.create_rectangle(x, y, x + larg, y + larg,
                                          fill="white")
                    x += larg
                    self.create_rectangle(x, y, x + larg, y + larg,
                                          fill=couleur.afficher_couleur())
                    x += larg
            x = 1
            y += larg


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
        scroll.pack(side=RIGHT, expand=YES, fill=BOTH, padx=2, pady=2)

    def ajouter_texte(self, action_a_ecrire):
        """Écrit le message demandé dans la zone historique de coup"""
        self.text.insert(END, action_a_ecrire + "\n")


class ScoreActuel(Label):
    def __init__(self, boss):
        Label.__init__(self, boss, font='Helvetica', text="score: ")

    def changer_score(self, score_a_ecrire):
        self.labelText = ('1.0', score_a_ecrire)


# ====== Définition des fenêtres popup ====== #

class FenJoueurs(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss, **kwargs)  # toplevel est fenêtre popup
        self.geometry("250x250+10+10")  # 300x300 donne dimension, 10x10 donne
        self.resizable(width=0, height=0)  # empeche resize
        Bouton(self, text="1 joueur", command=self.unjoueur).pack(pady=5, padx=10)
        Bouton(self, text="2 joueurs", command=self.deuxjoueurs).pack(pady=5, padx=10)

    def unjoueur(self):
        """ouvre une FenNiveauDif si 1 joueur choisi"""
        FenNiveauDif()
        self.destroy()

    def deuxjoueurs(self):
        """ouvre FenTypePartie si 2 joueurs"""
        FenTypePartie()
        self.destroy()


class FenNiveauDif(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le niveau de
    difficulté des parties à 1 joueur.
    """
    def __init__(self, **kwargs):
        Toplevel.__init__(self, **kwargs)
        self.geometry("250x250+10+10")
        self.resizable(width=0, height=0)
        Bouton(self, text="Normal", command=self.set_easy).pack(pady=15, padx=10)
        Bouton(self, text="Difficile", command=self.set_hard).pack(pady=15, padx=10)
        Bouton(self, text="Légendaire", command=self.set_legend).pack(pady=15, padx=10)

    def set_easy(self):
        global difficulte
        difficulte = "Normal"
        FenTypePartie()
        self.destroy()

    def set_hard(self):
        global difficulte
        difficulte = "Difficile"
        FenTypePartie()
        self.destroy()

    def set_legend(self):
        global difficulte
        difficulte = "Légendaire"
        FenTypePartie()
        self.destroy()


class FenTypePartie(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le type de partie
    soit classique ou personnalisée
    """
    def __init__(self, **kwargs):
        # TODO rien dedans bcuz fuckoff pour le moment
        Toplevel.__init__(self, **kwargs)
        self.geometry("250x250+10+10")
        self.resizable(width=0, height=0)
        #Glissoir(self, )
        Bouton(self, text="Jouer!", command=self.destroy).pack(pady=5, padx=10)


class FenPartiePerso(Toplevel):
    """
    Fenêtre satellite contenant les options de personnalisations lorsque le
    joueur choisi de faire une partie personnalisée
    """
    def __init__(self, boss, **kwargs):
        Toplevel.__init__(self, boss, **kwargs)
        self.geometry("500x500+10x10")


# ====== Définition de la fenêtre maîtresse ====== #

class Application(Tk):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        Tk.__init__(self)  # Constructeur de la classe maître
        self.difficulte = difficulte
        FenJoueurs(self)
        self.partie = Partie(self.difficulte)
        Bouton(self, text="Changer couleur", command=couleur.choisir_couleur())\
            .grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=2, column=0, rowspan=3, padx=5, pady=5)
        self.damier.bind("<Button-1>", self.pointeur)
        self.title("Brothello")
        self.barre_menu = Menubutton()
        # TODO servira à afficher coups possibles ou si trop dur à jouer un
        # TODO coup possible au hasard à la place du joueur
        Bouton(self, text="Voir les coups possibles", command=self.conseil)\
            .grid(row=0, column=0, padx=5, pady=5, sticky=W)
        Bouton(self, text="Nouvelle partie", command=self.nouvelle_partie)\
            .grid(row=1, column=2, padx=5, pady=5)
        Bouton(self, text="Abandonner", command=self.abandon)\
            .grid(row=2, column=2, padx=5, pady=5)
        ScoreActuel(self).grid(row=0, column=2)
        self.histo = Historique(self, height=21)
        self.histo.grid(row=3, column=2, padx=10, pady=5)


    def conseil(self):
        """ Dira à l'utilisateur les coups possibles """
        # TODO marche pas encore
        if self.difficulte == "Normal":
            coups_possibles = self.partie.coups_possibles
            if not coups_possibles or len(coups_possibles) < 1:
                coups_possibles = "aucun coup possible"
            self.histo.ajouter_texte("Les coups possibles sont:{}".format(
                coups_possibles))
        else:
            self.histo.ajouter_texte(" Aide seulement disponible en difficulté"
                                     " normale! Débrouillez-vous! ")

    def pointeur(self, event):
        """ Dessine une pièce (gros rond laid) où on clique"""
        # TODO plus belles pièces
        # TODO au centre des cases
        r = 25
        self.damier.create_oval(event.x-r, event.y-r, event.x+r, event.y+r,
                         fill='black')

    def abandon(self):
        self.histo.ajouter_texte("Le joueur {} abandonne la partie! ".format(
            self.partie.couleur_joueur_courant))

    @staticmethod
    def nouvelle_partie():
        """ Démarre une nouvelle partie (Redémarre l'application) """
        # TODO marche pas probablement parce que c'est pas le main qu'il repart
        python = executable
        execl(python, python, *argv)



# ====== Exécution du programme principal ====== #

le_jeu = Application()
le_jeu.mainloop()
