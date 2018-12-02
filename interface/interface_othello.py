from tkinter import *
from tkinter import colorchooser
from othello.partie import Partie
from time import sleep

difficulte = "Normale"
nb_cases = 8
nb_joueurs = 1
pasfini = True


# ======= TODO STYLE ======= #
# TODO 1- Faire barre d'outils en haut (Menubutton()?)
# TODO 2- Faire en sorte que clic dessine pièce MILIEU de la case
# TODO 3- Faire plus belle pièce
# TODO

#
# ======= TODO FONCTIONS ======= #
# TODO 1- convertir la position demandée sur le GUI Format (A, 1) en format
# TODO    (0, 0) avant de la valider ou de la jouer
# TODO 2- À chaque coup demandé, verifier avec self.partie.exceptions


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
        if None not in clr:
            self.color = clr[1]
        else:
            self.color = "black"


    def afficher_couleur(self):
        return str(self.color)


couleur = Color()


class Bouton(Button):
    """Classe définissant le style des boutons utilisés dans le jeu"""
    def __init__(self, boss, **kwargs):

        Button.__init__(self, boss, bg="dark grey", fg="black", bd=5,
                        activebackground=couleur.afficher_couleur(),
                        activeforeground="black",
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
        Canvas.__init__(self, boss, width=500, height=500,)
        self.larg = 500 // nb_cases
        #self.centre_cases = self.trouver_centres(self.larg)

    def trouver_centres(self, larg):
        #TODO pas fini, fait juste 1 rangée
        pass
        global nb_cases
        centres = []
        for carre in range(1, nb_cases+1):
            centre_carre = larg * carre
            centres.append(centre_carre)
        return centres

    def dessiner_carres(self):
        global nb_cases
        cote = 500 // nb_cases
        x, y = 1, 1
        print(cote)
        for i in range(1, nb_cases + 1):
            if i % 2 != 0:
                for j in range(nb_cases//2):
                    self.create_rectangle(x, y, x + cote, y + cote,
                                          fill=couleur.afficher_couleur())
                    x += cote
                    self.create_rectangle(x, y, x + cote, y + cote,
                                          fill="white")
                    x += cote
            else:
                for j in range(nb_cases//2):
                    self.create_rectangle(x, y, x + cote, y + cote,
                                          fill="white")
                    x += cote
                    self.create_rectangle(x, y, x + cote, y + cote,
                                          fill=couleur.afficher_couleur())
                    x += cote
            x = 1
            y += cote


class Historique(Frame):
    """Défini la zone de texte avec l'historique des coups joués"""
    def __init__(self, root, width=25, height=25):
        Frame.__init__(self, root, bd=2, bg='white',
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
        self.geometry("250x250+550+250")  # 300x300 dimension+posX+posY
        self.resizable(width=0, height=0)  # empeche resize
        self.attributes('-topmost', 'true')
        Bouton(self, text="1 joueur", command=self.unjoueur).pack(pady=5, padx=10)
        Bouton(self, text="2 joueurs", command=self.deuxjoueurs).pack(pady=5, padx=10)

    def unjoueur(self):
        """ouvre une FenNiveauDif si 1 joueur choisi"""
        global nb_joueurs
        nb_joueurs = 1
        FenNiveauDif()
        self.destroy()

    def deuxjoueurs(self):
        """ouvre FenTypePartie si 2 joueurs"""
        global nb_joueurs
        nb_joueurs = 2
        FenTypePartie()
        self.destroy()


class FenNiveauDif(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le niveau de
    difficulté des parties à 1 joueur.
    """
    def __init__(self, **kwargs):
        Toplevel.__init__(self, **kwargs)
        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
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
        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
        Bouton(self, text="Partie Classique", command=self.partie_classique).\
            pack(pady=5, padx=10)
        Bouton(self, text="Partie Personalisée", command=self.partie_perso).\
            pack(pady=5, padx=10)

    def partie_classique(self):
        global pasfini
        pasfini = False
        self.destroy()

    def partie_perso(self):
        FenPartiePerso()
        self.destroy()


class FenPartiePerso(Toplevel):
    """
    Fenêtre satellite contenant les options de personnalisations lorsque le
    joueur choisi de faire une partie personnalisée
    """
    def __init__(self, **kwargs):
        Toplevel.__init__(self, **kwargs)
        self.geometry("250x250+550+250")
        self.attributes('-topmost', 'true')
        Label(self, text="Combien de cases?").pack(padx=20, pady=20, fill=X)
        self.gliss = Glissoir(self, orient=HORIZONTAL, relief=SUNKEN, bd=2, from_=6,
                 to_=12, tickinterval=2, resolution=2)
        self.gliss.pack(padx=20, pady=20, fill=X)
        Bouton(self, text="jouer", command=self.set_perso).\
            pack(padx=20, pady=20, fill=X)

    def set_perso(self):
        """Envoie les paramètres choisis par l'utilisateur"""
        global nb_cases, pasfini
        nb_cases = self.gliss.get()
        pasfini = False
        self.destroy()


# ====== Définition de la fenêtre maîtresse ====== #

class Brothello(Tk):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        super().__init__()
        global difficulte, nb_cases, nb_joueurs
        self.title("Brothello")
        couleur.choisir_couleur()

        fond = "#"
        number = ['0', '1', '2', '3', '4', '4', '5', '6', '7', '8', '9']
        for i in range(1, 7):
            if couleur.color[i] not in number:
                fond += couleur.color[i]
            else:
                fond += "9"
        Brothello.config(self, bg=fond)
        self.go = Bouton(self, text="GO!", command=self.go)
        self.go.grid(row=0, column=0, padx=5, pady=5, sticky=W+E)
        FenJoueurs(self)

    def go(self):
        self.go.grid_remove()
        self.partie = Partie(nb_joueurs, difficulte, nb_cases)
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=2, column=0, rowspan=3, padx=5, pady=5)
        self.damier.bind("<Button-1>", self.pointeur)
        self.config(menu=TOP)
        self.geometry("800x600+550+250")
        self.resizable(height=0, width=0)
        # TODO servira à afficher coups possibles ou si trop dur à jouer un
        # TODO coup possible au hasard à la place du joueur
        Bouton(self, text="Voir les coups possibles", command=self.conseil)\
            .grid(row=0, column=0, padx=5, pady=5, sticky=W)
        Bouton(self, text="Nouvelle partie", command=self.nouvelle_partie)\
            .grid(row=1, column=2, padx=5, pady=5, sticky=W+E)
        Bouton(self, text="Abandonner", command=self.abandon)\
            .grid(row=2, column=2, padx=5, pady=5, sticky=W+E)
        ScoreActuel(self).grid(row=0, column=2, sticky=W)
        self.histo = Historique(self, height=21)
        self.histo.grid(row=3, column=2, padx=10, pady=5, sticky=W+E)
        self.commencer_partie()

    def commencer_partie(self):
        global nb_cases
        self.damier.dessiner_carres()

    def conseil(self):
        """ Dira à l'utilisateur les coups possibles """
        # TODO marche pas encore
        global difficulte
        if difficulte == "Normal":
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

    def nouvelle_partie(self):
        """ Démarre une nouvelle partie (Redémarre l'application) """
        # TODO marche pas probablement parce que c'est pas le main qu'il repart
        self.destroy()
        le_jeu = Brothello()
        le_jeu.mainloop()
