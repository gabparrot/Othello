from tkinter import *
from tkinter import colorchooser, messagebox, filedialog, ttk
from othello.partie import Partie
from othello.exceptions import ErreurPositionCoup, ErreurChoix
from othello.piece import Piece
from time import sleep
from winsound import *
from PIL import Image, ImageTk

# ====== Définition des classes globales de widgets de style ====== #


class Color:
    """
    Classe définissant la couleur utilisée dans le damier
    """

    # Couleurs du thème espace
    color = "#7b7f84"
    color2 = "#d9dadb"

    def choisir_couleur(self):
        """ Permet de changer la couleur avec un sélecteur de couleur """

        clr = colorchooser.askcolor(title="Modifier la couleur de la planche")
        if None not in clr and clr[1] not in ["#000000", "#FFFFFF", "#D3D3D3"]:
            self.color = clr[1]  # color hexadecimale
            rgb = clr[0]  # color redgreenblue
            # Faire 2e couleur un peu plus pale que 1ere
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            if r < 125 and g < 127 and b < 127:
                r = int(r * 2)
                g = int(g * 2)
                b = int(b * 2)
            else:
                if r > 0:
                    r = int(r//2)
                if g > 0:
                    g = int(g//2)
                if b > 0:
                    b = int(b//2)
            rgb = (int(r), int(g), int(b))
            self.color2 = "#%02x%02x%02x" % rgb
            if self.color2 in ["#000000", "#FFFFFF"]:
                self.color2 = self.color

    def afficher_couleur(self):
        """
        :return self.color: Retourne la couleur portée par l'attribut
            self.color
        """
        return str(self.color), str(self.color2)


couleur = Color()


class Glissoir(Scale):
    """ Classe définissant le style des glissoirs gradués """

    def __init__(self, boss, **kwargs):
        """ Constructeur des glissoirs """

        Scale.__init__(self, boss, bd=2, relief=SOLID, **kwargs)


class PlancheDeJeu(Canvas):
    """
    le damier, n'accepte présentement que des nombres pair de largeur de
    carrées, ex largeur de 6, 8, 10, 12 carrées de large
    """

    def __init__(self, boss):
        """ Constructeur du canevas avec la planche de jeu """

        Canvas.__init__(self, boss, width=500, height=500,
                        highlightthickness=0, relief=SUNKEN, borderwidth=0,
                        bg="black")
        self.nb_cases = boss.nb_cases
        self.largeur = boss.largeur

    def dessiner_carres(self):
        """ Dessine le damier en fonction des couleurs et du nombre de cases"""

        self.largeur = 500 // self.nb_cases
        x, y = 1, 1

        # Tracé des carrés
        for i in range(1, self.nb_cases + 1):
            liste_carres = []
            lettres_rangs = (chr(i + 64), chr(i + 65))

            coul1 = couleur.afficher_couleur()[0]
            coul2 = couleur.afficher_couleur()[1]
            if i % 2 == 0:
                coul1, coul2 = coul2, coul1

            for j in range(self.nb_cases // 2):
                num_col = (str(j * 2 + 1), str(j * 2 + 2))
                carre = self.create_rectangle(
                    x, y, x + self.largeur, y + self.largeur,
                    fill=coul1, outline='black',
                    tag=lettres_rangs[0] + num_col[0])
                liste_carres.append(carre)
                x += self.largeur
                carre = self.create_rectangle(
                    x, y, x + self.largeur, y + self.largeur,
                    fill=coul2, outline='black',
                    tag=lettres_rangs[0] + num_col[1])
                liste_carres.append(carre)
                x += self.largeur

            x = 1
            y += self.largeur

            # Écriture des coordonnées
            for carre in liste_carres:
                coords = self.coords(carre)
                txt = str(self.gettags(carre)[0])
                lettre = txt[0]
                chiffre = txt[1]
                if self.nb_cases == 6:
                    self.create_text(coords[0] + 2, coords[1] + 1, text=txt,
                                     fill='black',
                                     font='RobotoMono 8 bold', anchor=NW)
                elif self.nb_cases == 8:
                    self.create_text(coords[0] + 2, coords[1] + 1, text=txt,
                                     fill='black',
                                     font='RobotoMono 7 bold', anchor=NW)
                elif self.nb_cases == 10:

                    self.create_text(coords[0] + 2, coords[1] + 1, text=lettre,
                                     fill='black', font='RobotoMono 7 bold',
                                     anchor=NW)
                    self.create_text(coords[0] + self.largeur - 8, coords[1] +
                                     self.largeur - 10, fill='black',
                                     text=chiffre, font='RobotoMono 7 bold',
                                     anchor=NW)
                else:  # 12x12
                    self.create_text(coords[0] + 1, coords[1] + 1, text=lettre,
                                     fill='black', font='RobotoMono 7 bold',
                                     anchor=NW)
                    self.create_text(coords[0] + self.largeur - 8, coords[1] +
                                     self.largeur - 11, text=chiffre,
                                     fill='black', font='RobotoMono 7 bold',
                                     anchor=NW)


class Historique(ttk.Frame):
    """
    Défini la zone de texte avec l'historique des coups joués du thème bois
    """

    def __init__(self, root, width=25, height=25):
        """ Constructeur de l'historique de texte """

        ttk.Frame.__init__(self, root, width=width, height=height,
                           relief=SUNKEN)
        self.text = Text(self, font='Helvetica 12 bold', bg='#7b7f84', bd=1,
                         width=width, height=height, wrap=WORD)
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        scroll.pack(side=RIGHT, expand=YES, fill=BOTH, padx=(0, 2), pady=2)

    def ajouter_texte(self, action_a_ecrire):
        """
        Écrit le message demandé dans la zone historique de coup et ramène la
        barre de défilement à la fin de l'historique
        """

        self.text.insert(END, action_a_ecrire + "\n")
        self.text.see("end")


# ====== Définition des fenêtres popup ====== #

class FenJoueurs(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """

    def __init__(self, boss):
        """ Constructeur de FenJoueurs """
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("200x200+550+250")  # 300x300 dimension+posX+posY
        self.resizable(width=0, height=0)  # Empêche resize
        self.attributes('-topmost', 'true')  # Reste par dessus fen principale

        self.fond_label = Label(self, image=boss.fond)
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)
        ttk.Button(self, text=" 1 joueur  ",
                   command=lambda: self.donner_nb(1)).\
            grid(row=0, column=0, pady=(50, 20), padx=40)
        ttk.Button(self, text=" 2 joueurs  ",
                   command=lambda: self.donner_nb(2)).\
            grid(row=1, column=0, pady=20, padx=60)

    def donner_nb(self, nb: int):
        """ Donne le nombre de joueurs choisi à self.nb et ferme la fenêtre """

        self.nb = nb
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenNiveauDif(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le niveau de
    difficulté des parties à 1 joueur.
    """

    def __init__(self, boss):
        """ Constructeur de FenNiveauDif """

        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("200x200+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')

        self.fond_label = Label(self, image=boss.fond)
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Button(self, text="Facile",
                   command=lambda: self.donner_diff('facile')).\
            grid(row=0, column=1, pady=(20, 10), padx=60)
        ttk.Button(self, text="Normale",
                   command=lambda: self.donner_diff('normale')).\
            grid(row=1, column=1, pady=10, padx=60)
        ttk.Button(self, text="Difficile",
                   command=lambda: self.donner_diff('difficile')).\
            grid(row=2, column=1, pady=10, padx=60)
        ttk.Button(self, text="Légendaire",
                   command=lambda: self.donner_diff('legendaire')).\
            grid(row=3, column=1, pady=10, padx=60)

    def donner_diff(self, diff: str):
        """ Donne la valeur choisie à self.diff et ferme la fenêtre """

        self.diff = diff
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenTypePartie(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le type de partie
    soit classique ou personnalisée
    """

    def __init__(self, boss):
        """ Constructeur de FenTypePartie """

        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("200x200+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')

        self.fond_label = Label(self, image=boss.fond)
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Button(self, text="  Partie Classique  ",
                   command=lambda: self.donner_type('classique')).\
            grid(row=0, column=0, pady=(50, 20), padx=40)
        ttk.Button(self, text="Partie Personalisée",
                   command=lambda: self.donner_type('perso')).\
            grid(row=1, column=0, pady=20, padx=40)

    def donner_type(self, type_partie: str):
        """
        Donne la valeur 'classique' à self.type_partie et ferme la fenêtre
        """

        self.type_partie = type_partie
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenPartiePerso(Toplevel):
    """
    Fenêtre satellite contenant les options de personnalisations lorsque le
    joueur choisi de faire une partie personnalisée
    """

    def __init__(self, boss):
        """ Constructeur de FenPartiePerso """

        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("250x250+550+250")
        self.attributes('-topmost', 'true')

        self.fond_label = Label(self, image=boss.fond)
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(self, text="Combien de cases?", bg=couleur.color2, bd=2,
              relief=SOLID).pack(padx=20, pady=20, fill=X)
        self.gliss = Glissoir(self, orient=HORIZONTAL,
                              from_=6, to_=12, tickinterval=2,
                              resolution=2)
        self.gliss.pack(padx=20, pady=20, fill=X)
        ttk.Button(self, text="Jouer!",
                   command=self.donner_nb_cases).\
            pack(padx=20, pady=20, fill=X)

    def donner_nb_cases(self):
        """
        Envoie les paramètres choisis par l'utilisateur et ferme la fenêtre
        """

        self.cases = self.gliss.get()
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class ChoixTheme(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """

    def __init__(self, boss):
        """ Constructeur de FenJoueurs """
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("200x200+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')

        self.fond_label = Label(self, image=boss.fond)
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Button(self, text=" Forest  ",
                   command=lambda: self.donner_theme('forest')).\
            grid(row=0, column=0, pady=(30, 17), padx=40)
        ttk.Button(self, text=" Redwood",
                   command=lambda: self.donner_theme('redwood')).\
            grid(row=1, column=0, pady=17, padx=40)
        ttk.Button(self, text=" Espace ",
                   command=lambda: self.donner_theme('espace')).\
            grid(row=2, column=0, pady=17, padx=60)

    def donner_theme(self, theme: str):
        """
        Donne la valeur bois à self.theme, l'applique et ferme la fenêtre
        """

        self.theme = theme
        self.grab_release()
        self.master.focus_set()
        self.destroy()


# ************************************************ #
# ====== Définition de la fenêtre maîtresse ====== #
# ******************** de ************************ #
# ================= BROTHELLO ==================== #
# ************************************************ #

class Brothello(Tk):
    """ Classe de la fenêtre principale du jeu """

    def __init__(self, theme=None):
        """Constructeur de la fenêtre principale"""

        super().__init__()

        # Caractérisiques de la fenêtre principale
        self.title("Brothello")
        self.geometry("850x625+550+250")
        self.resizable(height=0, width=0)

        # Évite crash si quitte avec 'X', fait exit() au lieu de self.destroy()
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.occupe = False

        if theme:
            self.theme = theme  # conserve theme choisi
        else:
            self.theme = 'espace'  # par défaut

        self.anciennes_pieces = {}  # dictionnaire pieces tour precedent
        self.mettre_theme()

        # Menus
        self.creer_menus()

        # Définition des caractéristiques de la partie par défaut
        self.nb_cases = 8
        self.difficulte = 'normale'
        self.type_partie = 'perso'
        self.nb_joueurs = 1
        self.largeur = 500//self.nb_cases
        self.initialiser_damier()
        self.update_idletasks()

        # # Popups choix options du jeu
        self.poser_questions()

        # Création de l'instance du jeu et liste des coups possibles
        self.initialiser_damier()
        self.partie = Partie(self.nb_joueurs, self.difficulte, self.nb_cases)
        self.placer_pieces()

        # Activation des éléments de l'interface
        self.bout_conseil.config(state=NORMAL)

    def creer_menus(self):
        """ Crée la barre de menus / sous-menus de la fenêtre principale """

        self.mainmenu = Menu(self)
        first_menu = Menu(self.mainmenu, tearoff=0)
        first_menu.add_command(
            label="Nouvelle partie", command=self.nouvelle_partie)
        first_menu.add_command(
            label="Ouvrir", command=self.charger)
        first_menu.add_command(
            label="Enregistrer sous", command=self.sauvegarder)
        first_menu.add_command(
            label="Abandonner la partie", command=self.abandon)
        first_menu.add_command(label='Quitter', command=self.quitter)
        second_menu = Menu(self.mainmenu, tearoff=0)
        second_menu.add_command(label='Changer la couleur du damier',
                                command=self.action_bouton_couleur)
        second_menu.add_command(label='Changer le thème',
                                command=self.choisir_theme)
        third_menu = Menu(self.mainmenu, tearoff=0)
        third_menu.add_command(label="Comment jouer", command=self.aide)
        self.mainmenu.add_cascade(label="Fichier", menu=first_menu)
        self.mainmenu.add_cascade(label='Options', menu=second_menu)
        self.mainmenu.add_cascade(label="Aide", menu=third_menu)
        Brothello.config(self, menu=self.mainmenu)

    def poser_questions(self):
        """ Popups choix options du jeu """
        try:
            # Choix nombre joueurs
            fen_joueur = FenJoueurs(self)
            self.wait_window(fen_joueur)
            if fen_joueur.nb not in [1, 2]:
                raise ErreurChoix("Erreur. Fin de la partie.")
            self.nb_joueurs = fen_joueur.nb

            # Si 1 joueur choix difficulte
            if self.nb_joueurs == 1:
                fen_diff = FenNiveauDif(self)
                self.wait_window(fen_diff)
                if fen_diff.diff not in ['facile', 'normale',
                                         'difficile', 'legendaire']:
                    raise ErreurChoix("Erreur. Fin de la partie.")
                self.difficulte = fen_diff.diff

            # Choix partie classique ou personnalisee
            fen_type = FenTypePartie(self)
            self.wait_window(fen_type)
            if fen_type.type_partie not in ['classique', 'perso']:
                raise ErreurChoix("Erreur. Fin de la partie.")
            self.type_partie = fen_type.type_partie

            # 8 cases si type classique, sinon choix nb cases
            if self.type_partie == 'classique':
                self.nb_cases = 8
            elif self.type_partie == 'perso':
                fen_perso = FenPartiePerso(self)
                self.wait_window(fen_perso)
                self.nb_cases = fen_perso.cases

        except(ErreurChoix, AttributeError):
            box_fin = messagebox.askyesno('Erreur! Mauvaise réponse',
                                          'Erreur dans les réponses, voulez-'
                                          'vous recommencer?')
            if box_fin:
                self.nouvelle_partie()
            else:
                exit()

    def initialiser_damier(self):
        """
        Crée le cavevas de la planche de jeu.
        """

        self.largeur = 500//self.nb_cases
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=0, column=0, rowspan=2, padx=(20, 10), pady=(90,
                                                                          10))
        self.damier.bind("<Button-1>", self.pointeur)
        self.damier.dessiner_carres()

    # ====== Fonctions des widgets ====== #

    def action_bouton_couleur(self):
        """
        Permet de changer de couleur avec le selecteur de couleur, puis
        redessine le damier et les pieces en fonction de cette couleur
        """

        couleur.choisir_couleur()
        self.damier.dessiner_carres()
        self.placer_pieces()

    def choisir_theme(self):
        """
        Ouvre un popup de choix de thème et l'applique
        """

        self.bout_conseil.config(state=DISABLED)
        try:
            fen_theme = ChoixTheme(self)
            self.wait_window(fen_theme)
            if fen_theme.theme not in ['forest', 'redwood', 'espace']:
                raise ErreurChoix("Erreur dans le choix. Aucun changement "
                                  "appliqué.")
            self.theme = fen_theme.theme
            self.mettre_theme()

        except (ErreurChoix, AttributeError):
            self.messagebox.ERROR("Une erreur s'est produite. Aucun changement"
                                  " n'a été apporté au thème.")
        finally:
            self.bout_conseil.config(state=NORMAL)

    def mettre_theme(self):
        """ Applique le thème courant en definissant les Widgets """

        # TODO changer star.gif pour PNG puis enlever le if else ici
        if self.theme == 'espace':
            theme_file = 'star.gif'
        else:
            theme_file = self.theme + '.png'

        # Fenêtre principale
        self.fond = PhotoImage(file=theme_file)
        self.fond_label = Label(self, image=self.fond)
        self.fond_label.image = self.fond_label
        self.fond_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Widgets esclaves
        self.frame1 = Frame(self)
        self.frame1.grid(row=1, column=1, padx=(10, 20), pady=(3, 10),
                         sticky=NW)

        if hasattr(self, 'bout_conseil'):
            self.bout_conseil.grid_remove()

        self.histo = Historique(self, height=21)
        self.histo.grid(row=1, column=1, padx=(10, 20), pady=(3, 10),
                        sticky=S)
        self.histo.text.config(bg='#dbc0c0')

        if self.theme == 'redwood':
            couleur.color = '#400000'
            couleur.color2 = '#800000'
            self.photo_bouton = PhotoImage(file="bouton_bois.png")

        elif self.theme == 'espace':
            # Fenêtre principale
            couleur.color = "#7b7f84"
            couleur.color2 = "#d9dadb"

            # Widgets esclaves
            self.histo.text.config(bg='#7b7f84')
            self.photo_bouton = PhotoImage(file="bouton_espace.png")

        elif self.theme == 'forest':
            # Fenêtre principale
            couleur.color = "#ded3ed"
            couleur.color2 = "#9071ba"

            # Widgets esclaves
            self.histo.text.config(bg='#ded3ed')
            self.photo_bouton = PhotoImage(file="bouton_forest.png")

        self.bout_conseil = Button(self.frame1, image=self.photo_bouton,
                                   command=self.conseil, state=DISABLED)
        self.bout_conseil.grid(row=1, column=1, sticky=NW)
        self.bout_conseil.image = self.photo_bouton

        if len(self.anciennes_pieces) > 0:  # Si partie en cours, met score
            self.changer_score()
            self.initialiser_damier()
            self.placer_pieces()
        self.update_idletasks()

    def changer_score(self):
        """ Calcul le score à chaque tour."""

        self.pieces_noires = 0
        self.pieces_blanches = 0

        for case in self.partie.planche.liste_cases:
            if self.partie.planche.get_piece(case):
                if self.partie.planche.get_piece(case).couleur == "blanc":
                    self.pieces_blanches += 1
                elif self.partie.planche.get_piece(case).couleur == "noir":
                    self.pieces_noires += 1

        self.score = "Score : \nJoueur noir : {} \nJoueur blanc : {}".\
            format(self.pieces_noires, self.pieces_blanches)

        self.histo.ajouter_texte("\n" + self.score + "\n")

    def placer_pieces(self):
        """ Dessine les pieces nouvelles ou modifies """
        self.damier.delete("all")
        self.damier.dessiner_carres()
        for piece in self.anciennes_pieces:
            self.dessiner_piece(piece, self.anciennes_pieces[piece].couleur)
        for piece in self.partie.planche.cases:
            if piece not in self.anciennes_pieces:
                # Placer au centre de la case
                self.couleur_piece = self.partie.planche.cases[piece].couleur
                if self.couleur_piece == "blanc":
                    self.couleur_piece = "white"
                elif self.couleur_piece == "noir":
                    self.couleur_piece = "black"

                self.anciennes_pieces[piece] = Piece(self.couleur_piece)
                self.dessiner_piece(piece, self.couleur_piece)
                self.damier.update_idletasks()
                self.plop()
                sleep(0.35)

        for piece in self.partie.planche.cases:
            if piece in self.anciennes_pieces:
                if self.partie.planche.cases[piece].couleur != \
                        self.anciennes_pieces[piece].couleur:
                    # Placer au centre de la case
                    couleur_piece = self.partie.planche.cases[piece].couleur
                    if couleur_piece == "blanc":
                        couleur_piece = "white"
                    elif couleur_piece == "noir":
                        couleur_piece = "black"
                    del(self.anciennes_pieces[piece])
                    self.anciennes_pieces[piece] = Piece(self.couleur_piece)
                    self.dessiner_piece(piece, couleur_piece)
                    self.damier.update_idletasks()
                    self.blip()
                    sleep(0.35)

        for piece in self.partie.planche.cases:
            # Placer au centre de la case
            couleur_piece = self.partie.planche.cases[piece].couleur
            if couleur_piece == "blanc":
                couleur_piece = "white"
            elif couleur_piece == "noir":
                couleur_piece = "black"

            if couleur_piece not in ['white', 'black']:
                self.dessiner_piece(piece, couleur_piece)

    def dessiner_piece(self, position: tuple, couleur_piece: str):
        """ Trace la pièce dans le canevas"""
        r = self.largeur
        mid_x = position[0] * self.largeur + self.largeur // 2
        mid_y = position[1] * self.largeur + self.largeur // 2

        if position in self.anciennes_pieces:
            if self.anciennes_pieces[position].couleur in ['noir', 'black']:
                img = ImageTk.PhotoImage(Image.open('noir3d.png').
                                         resize((r, r)))
            else:
                img = ImageTk.PhotoImage(Image.open('blanc3d.png').
                                         resize((r, r)))
            self.anciennes_pieces[position].image = img
            self.damier.create_image(
                mid_x, mid_y, anchor=CENTER,
                image=self.anciennes_pieces[position].image)
        else:
            r = round(self.largeur / 5 * 1.75)
            self.damier.create_oval(mid_x - r, mid_y - r + 1, mid_x + r - 1,
                                    mid_y + r - 5, fill=couleur_piece,
                                    outline='black')

    def tour_humain(self, case_clic: tuple):
        """ Joue le coup du clic humain """

        self.partie.tour(case_clic)
        ligne_jouee = chr(case_clic[1] + 65)
        col_jouee = str(case_clic[0] + 1)
        coup_jouer = ligne_jouee + col_jouee
        self.histo.ajouter_texte(f"Joueur {self.partie.joueur_courant.couleur}"
                                 f" a joué en {coup_jouer}")
        self.changer_score()

    def pointeur(self, event: EventType):
        """
        Établit dans quelle case le joueur a cliqué, joue son coup ou lui dit
        si ce n'est pas possible et pourquoi. Envoie l'informations à Partie
        pour modifier les données. Effectue le changement de joueurs. Si ce
        joueur est un ordinateur, lui fait aussi joueur son tour avant
        d'attendre un nouveau clic

        :param event: Un clic sur le canevas de la planche de jeu
        """

        # coordonnées (x, y) de la case en range (0, nb_cases) ex (0, 4)
        case_clic = (event.x//self.largeur, event.y//self.largeur)
        ligne_jouee = chr(case_clic[1] + 65)
        col_jouee = str(case_clic[0] + 1)
        coup_jouer = ligne_jouee + col_jouee
        self.histo.ajouter_texte(f"Coup demandé en {coup_jouer}")

        # Valider puis jouer le coup
        if self.valider_coup(case_clic):
            self.tour_humain(case_clic)
            self.placer_pieces()
            self.update_idletasks()
            sleep(0.5)
            self.changer_joueur()
            if self.partie.joueur_courant.obtenir_type_joueur() == \
                    'Ordinateur':
                self.tour_ordi()
                self.placer_pieces()
                sleep(0.2)
                self.changer_joueur()
        else:
            self.histo.ajouter_texte(f"Coup en {coup_jouer} refusé")

    def changer_joueur(self):
        """
        Fait appelle à partie.changement_joueur() pour changer les variables
        dans le jeu, met à jour l'historique, et vérifie si le joueur courant
        doit passer son tour avec .
        """

        self.partie.changement_joueur()
        self.histo.ajouter_texte("Tour du joueur {}".format(
            self.partie.couleur_joueur_courant))
        self.verif_passer_tour()

    def verif_passer_tour(self):
        """ vérifie si le joueur courant
        doit passer son tour. La cas échéant, un message est affiché et la
        fonction s'appelle elle-même pour rechanger de joueur. """

        if self.partie.verifier_tour_a_passer():
            if self.partie.joueur_courant.obtenir_type_joueur() == 'Humain':
                txt = "Aucun coup possible! Vous passez votre tour!"
                messagebox.showinfo('Aucun coup possible', txt)
            else:
                txt = "L'ordinateur n'a aucun coup possible. Il passe donc " \
                      "son tour!"
                messagebox.showinfo('Aucun coup possible', txt)

            self.histo.ajouter_texte(txt)
            self.verifier_fin()
            self.changer_joueur()

    def verifier_fin(self):
        """
        Appelle partie.partie_terminee() pour verifier si les conditions de fin
        de partie sont remplies. Le cas échéant, un message et un son
        sont affichés en fonction du vainqueur, et on demande si le joueur
        souhaite jouer une nouvelle partie.
        """

        if self.partie.partie_terminee():
            victoire = self.partie.determiner_gagnant()
            if victoire[0]:
                sleep(0.2)
                self.update_idletasks()
                self.woohoo()
            elif not victoire[0]:
                sleep(0.2)
                self.update_idletasks()
                self.gameover()

            self.histo.ajouter_texte(victoire[1])
            txt_fin = victoire[1] + \
                '\nVoulez vous jouer une nouvelle partie?'
            box_fin = messagebox.askyesno('Partie teminée!', txt_fin)
            if not box_fin:
                exit()
            elif box_fin:
                self.nouvelle_partie()

    def tour_ordi(self):
        """ Fait jouer l'ordinateur """

        if self.partie.joueur_courant.obtenir_type_joueur() == 'Ordinateur':
            coup_ordi = self.partie.tour((-1, -1))
            ligne_jouee = chr(coup_ordi[1] + 65)
            col_jouee = str(coup_ordi[0] + 1)
            coup_jouer = ligne_jouee + col_jouee
            self.histo.ajouter_texte(
                f"Joueur {self.partie.joueur_courant.couleur}"
                f" a joué en {coup_jouer}")
            self.changer_score()

    def valider_coup(self, position: tuple):
        """ Vérifie si coup valide, affiche msg sinon """
        msg = ""
        try:
            if position in self.partie.coups_du_tour[1]:
                msg = "Impossible, vous ne pouvez pas mettre une pièce par" \
                      " dessus une autre! "
                raise ErreurPositionCoup
            if position in self.partie.coups_du_tour[2]:
                msg = "Coup invalide. Aucune pièce ennemie ne serait mangée! "
                raise ErreurPositionCoup
            if position not in self.partie.coups_du_tour[0]:
                msg = "Une erreur inconnue s'est produite avec le coup " \
                      "demandé. Veuillez réessayer."
                raise ErreurPositionCoup
            return True
        except ErreurPositionCoup:
            messagebox.showinfo("Coup invalide", msg)
            return False

    def conseil(self):
        """ Affiche à l'utilisateur les coups possibles """
        self.bout_conseil.config(state=DISABLED)
        if self.difficulte in ["facile", "normale"]:
            coups_possibles = self.partie.coups_possibles
            if not coups_possibles or len(coups_possibles) < 1:
                self.histo.ajouter_texte("Aucun coup possible!")
            for coup in coups_possibles:
                couleur_piece = 'light green'
                self.dessiner_piece(coup, couleur_piece)
                self.hint()
                self.damier.update_idletasks()
                sleep(0.55)
            self.damier.dessiner_carres()
            self.placer_pieces()
        else:
            self.histo.ajouter_texte("Aide seulement disponible en difficulté"
                                     " facile ou normale! Débrouillez-vous! "
                                     "\n")

        self.bout_conseil.config(state=ACTIVE)

    def abandon(self):
        """
        Concède la victoire à l'ennemi et demande si le joueur souhaite jouer
        une autre partie
        """

        self.histo.ajouter_texte("Le joueur {} abandonne la partie! ".format(
            self.partie.couleur_joueur_courant))
        txt_fin = (f"Joueur {self.partie.couleur_joueur_courant} "
                   f"abandonne la partie! \nVoulez vous jouer une nouvelle "
                   f"partie?")
        self.changer_joueur()
        if self.partie.joueur_courant.obtenir_type_joueur() == "Humain":
            sleep(0.1)
            self.woohoo()
            self.update_idletasks()
        else:
            sleep(0.1)
            self.gameover()
            self.update_idletasks()
        box_fin = messagebox.askyesno('Partie teminée!', txt_fin)
        if not box_fin:
            exit()
        elif box_fin:
            self.nouvelle_partie()

    @staticmethod
    def quitter():
        """ Quitte le jeu """
        exit()

    def nouvelle_partie(self):
        """ Démarre une nouvelle partie (Redémarre l'application) """

        self.bout_conseil.config(state=DISABLED)
        self.anciennes_pieces.clear()
        self.poser_questions()
        self.partie = Partie(self.nb_joueurs, self.difficulte, self.nb_cases)
        self.initialiser_damier()
        self.update_idletasks()
        self.placer_pieces()
        self.bout_conseil.config(state=NORMAL)

    @staticmethod
    def aide():
        aidemsg = ("A son tour de jeu, le joueur doit poser un pion de "
                   "sa couleur sur une case vide de l’othellier, adjacente "
                   "à un pion adverse. Il doit également, en posant son pion,"
                   " encadrer un ou plusieurs pions adverses entre le pion"
                   " qu’il pose et un pion à sa couleur, déjà placé sur"
                   " l’othellier. Il retourne alors de sa couleur le ou les "
                   "pions qu’il vient d’encadrer. Les pions ne sont ni retirés"
                   " de l’othellier, ni déplacés d’une case à l’autre.\n\n"
                   "Source: http://www.ffothello.org/othello/regles-du-jeu/")
        messagebox.showinfo(title="Comment jouer", message=aidemsg)

        # ====== Définition des effets sonores ====== #

    @staticmethod
    def plop():
        try:
            PlaySound('plop.wav', SND_FILENAME | SND_ASYNC)

        except RuntimeError:
            print("RUNTIME ERROR SON ÉVITÉE")
            PlaySound('blip.wav', SND_FILENAME | SND_PURGE)
            PlaySound('plop.wav', SND_FILENAME | SND_PURGE)
            PlaySound('woohoo.wav', SND_FILENAME | SND_PURGE)
            PlaySound('gameover.wav', SND_FILENAME | SND_PURGE)
            PlaySound('hint.wav', SND_FILENAME | SND_PURGE)

    @staticmethod
    def blip():
        try:
            PlaySound('blip.wav', SND_FILENAME | SND_ASYNC)

        except RuntimeError:
            print("RUNTIME ERROR SON ÉVITÉE")
            PlaySound('blip.wav', SND_FILENAME | SND_PURGE)
            PlaySound('plop.wav', SND_FILENAME | SND_PURGE)
            PlaySound('woohoo.wav', SND_FILENAME | SND_PURGE)
            PlaySound('gameover.wav', SND_FILENAME | SND_PURGE)
            PlaySound('hint.wav', SND_FILENAME | SND_PURGE)

    @staticmethod
    def woohoo():
        try:

            PlaySound('woohoo.wav', SND_FILENAME | SND_ASYNC | SND_NOSTOP)

        except RuntimeError:
            print("RUNTIME ERROR SON ÉVITÉE")
            PlaySound('blip.wav', SND_FILENAME | SND_PURGE)
            PlaySound('plop.wav', SND_FILENAME | SND_PURGE)
            PlaySound('woohoo.wav', SND_FILENAME | SND_PURGE)
            PlaySound('gameover.wav', SND_FILENAME | SND_PURGE)

    @staticmethod
    def gameover():
        try:

            PlaySound('gameover.wav', SND_FILENAME | SND_ASYNC | SND_NOSTOP)

        except RuntimeError:
            print("RUNTIME ERROR SON ÉVITÉE")
            PlaySound('blip.wav', SND_FILENAME | SND_PURGE)
            PlaySound('plop.wav', SND_FILENAME | SND_PURGE)
            PlaySound('woohoo.wav', SND_FILENAME | SND_PURGE)
            PlaySound('gameover.wav', SND_FILENAME | SND_PURGE)
            PlaySound('hint.wav', SND_FILENAME | SND_PURGE)

    @staticmethod
    def hint():
        """ Son lors de l'apparation des pièces vertes pour conseil() """
        try:
            PlaySound('hint.wav', SND_FILENAME | SND_ASYNC)

        except RuntimeError:
            print("RUNTIME ERROR SON ÉVITÉE")
            PlaySound('blip.wav', SND_FILENAME | SND_PURGE)
            PlaySound('plop.wav', SND_FILENAME | SND_PURGE)
            PlaySound('woohoo.wav', SND_FILENAME | SND_PURGE)
            PlaySound('gameover.wav', SND_FILENAME | SND_PURGE)
            PlaySound('hint.wav', SND_FILENAME | SND_PURGE)

    # ====== Getters et Setters d'options de partie ====== #
    @property
    def nb_joueurs(self):
        return self.__nb_joueurs

    @nb_joueurs.setter
    def nb_joueurs(self, nb: int):
        self.__nb_joueurs = nb

    @property
    def difficulte(self):
        return self.__difficulte

    @difficulte.setter
    def difficulte(self, diff: str):
        self.__difficulte = diff

    @property
    def type_partie(self):
        return self.__type_partie

    @type_partie.setter
    def type_partie(self, type_partie: str):
        self.__type_partie = type_partie

    @property
    def nb_cases(self):
        return self.__nb_cases

    @nb_cases.setter
    def nb_cases(self, nb: int):
        self.__nb_cases = nb
    # ====== Fonctions de sauvegarde / chargement ===== #

    def charger(self):
        self.filename = filedialog.askopenfilename(title="Ouvrir le fichier",
                                                   filetypes=[(".txt",
                                                               "*.txt")])

        f = open(self.filename, "r")

        self.partie.couleur_joueur_courant = f.readline().strip("\n")

        self.partie.planche.cases.clear()
        self.anciennes_pieces.clear()
        self.partie.nb_cases = 8
        self.partie.difficulte = 'normale'
        self.partie.nb_joueurs = 2
        self.nb_cases = 8
        self.difficulte = 'normal'
        self.type_partie = 'classique'
        self.nb_joueurs = 2
        self.largeur = 500//self.nb_cases
        self.initialiser_damier()
        self.damier.update_idletasks()

        if f.readline() == "True":
            self.partie.tour_precedent_passe = True
        else:
            self.partie.tour_precedent_passe = False

        if f.readline() == "True":
            self.partie.deux_tours_passes = True
        else:
            self.partie.deux_tours_passes = False

        if f.readline() == "Ordinateur":
            self.partie.joueur_noir = self.partie.creer_joueur("Ordinateur",
                                                               "noir")
        else:
            self.partie.joueur_noir = self.partie.creer_joueur("Humain",
                                                               "noir")

        if f.readline() == "Ordinateur":
            self.partie.joueur_blanc = self.partie.creer_joueur("Ordinateur",
                                                                "blanc")
        else:
            self.partie.joueur_blanc = self.partie.creer_joueur("Humain",
                                                                "blanc")

        if self.partie.couleur_joueur_courant == "noir":
            self.partie.joueur_courant = self.partie.joueur_noir
        else:
            self.partie.joueur_courant = self.partie.joueur_blanc

        self.partie.planche.charger_dune_chaine(f.read())

        f.close()

        self.placer_pieces()
        txt = "Tour du joueur {}".format(
            self.partie.couleur_joueur_courant)
        self.histo.ajouter_texte(txt)
        messagebox.showinfo(" Partie chargée ", txt)
        self.changer_score()
        self.partie.determiner_coups_du_tour()
        self.verifier_fin()
        self.verif_passer_tour()

    def sauvegarder(self):

        self.ma_partie = filedialog.asksaveasfile(
            title="Sauvegarder", mode='w', defaultextension=".txt")

        print(self.ma_partie)
        fichier = self.ma_partie
        fichier.write(self.partie.couleur_joueur_courant + "\n" +
                      str(self.partie.tour_precedent_passe) + "\n" +
                      str(self.partie.deux_tours_passes) + "\n" +
                      str(self.partie.joueur_blanc.obtenir_type_joueur()) +
                      "\n" +
                      str(self.partie.joueur_noir.obtenir_type_joueur()) +
                      "\n" +
                      self.partie.planche.convertir_en_chaine())

        fichier.close()
