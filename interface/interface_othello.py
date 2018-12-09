from tkinter import *
from tkinter import colorchooser, messagebox
from othello.partie import Partie
from othello.exceptions import ErreurPositionCoup
from time import sleep



# ======= TODO STYLE ======= #
# TODO 1- Faire barre d'outils en haut (Menubutton()?)
# TODO 3- Faire plus belle pièce
#
# ======= TODO FONCTIONS ======= #
# TODO 1- convertir la position demandée sur le GUI Format (A, 1) en format
# TODO    (0, 0) avant de la valider ou de la jouer


# === Définition des objets esclaves et de leurs éléments de style === #
class Color:
    """
    Classe définissant la couleur utilisée dans le damier
    """

    color = "deepskyblue2"  # RGB(0,178,238)

    color2 = "#%02x%02x%02x" % (0, 178//2, 238//2)

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
            if r < 80 and g < 80 and b < 80:
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
            print(self.color2)
            if self.color2 in ["#000000", "#FFFFFF", "#D3D3D3"]:
                self.color2 = self.color
        else:
            self.color = "deepskyblue2"
            self.color2 = "#%02x%02x%02x" % (0, 178//3*2, 238//3*2)

    def afficher_couleur(self):
        """
        :return self.color: Retourne la couleur portée par l'attribut
            self.color
        """
        return str(self.color), str(self.color2)


couleur = Color()


class Bouton(Button):
    """ Classe définissant le style des boutons utilisés dans le jeu """

    def __init__(self, boss, **kwargs):
        """ Constructeur des boutons"""

        Button.__init__(self, boss, bg="dark grey", fg="black", bd=5,
                        activebackground="grey",
                        activeforeground="white",
                        font='Helvetica', **kwargs)


class Glissoir(Scale):
    """ Classe définissant le style des glissoirs gradués """

    def __init__(self, boss, **kwargs):
        """ Constructeur des glissoirs """
        Scale.__init__(self, boss, **kwargs)


class PlancheDeJeu(Canvas):
    """
    le damier, n'accepte présentement que des nombres pair de largeur de
    carrées, ex largeur de 6, 8, 10, 12 carrées de large
    """

    def __init__(self, boss):
        """ Constructeur du canevas avec la planche de jeu """

        Canvas.__init__(self, boss, width=500, height=500, highlightthickness=0
                        , relief=SUNKEN)
        self.nb_cases = boss.nb_cases
        self.largeur = boss.largeur

    def dessiner_carres(self):
        """ Dessine le damier en fonction des couleurs et du nombre de cases"""

        self.largeur = 500 // self.nb_cases
        x, y = 1, 1
        for i in range(1, self.nb_cases + 1):
            liste_carres = []
            lettres_rangs = (chr(i + 64), chr(i + 65))
            print(lettres_rangs)
            if i % 2 != 0:
                for j in range(self.nb_cases//2):
                    num_col = (str(j*2+1), str(j*2+2))
                    carre = self.create_rectangle(x, y, x + self.largeur, y +
                                          self.largeur,
                                          fill=couleur.afficher_couleur()[0],
                                          outline='black',
                                          tag=lettres_rangs[0] + num_col[0])
                    liste_carres.append(carre)
                    x += self.largeur
                    carre = self.create_rectangle(x, y, x + self.largeur, y +
                                          self.largeur,
                                          fill=couleur.afficher_couleur()[1],
                                          outline='black',
                                          tag=lettres_rangs[0] + num_col[1])
                    liste_carres.append(carre)
                    x += self.largeur
            else:
                for j in range(self.nb_cases//2):
                    num_col = (str(j * 2 + 1), str(j * 2 + 2))
                    carre = self.create_rectangle(x, y, x + self.largeur, y +
                                          self.largeur,
                                          fill=couleur.afficher_couleur()[1],
                                          outline='black',
                                          tag=lettres_rangs[0] + num_col[0])
                    liste_carres.append(carre)
                    x += self.largeur
                    carre = self.create_rectangle(x, y, x + self.largeur, y +
                                          self.largeur,
                                          fill=couleur.afficher_couleur()[0],
                                          outline='black',
                                          tag=lettres_rangs[0] + num_col[1])
                    liste_carres.append(carre)
                    x += self.largeur
            x = 1
            y += self.largeur
            for carre in liste_carres:
                coords = self.coords(carre)
                txt = str(self.gettags(carre)[0])
                self.create_text(coords[0]+2, coords[1]+1, text=txt,
                                 font='Roboto 7 bold', anchor=NW)


class Historique(Frame):
    """ Défini la zone de texte avec l'historique des coups joués """

    def __init__(self, root, width=25, height=25):
        """ Constructeur de l'historique de texte """

        Frame.__init__(self, root, bd=2, bg='white',
                       width=width, height=height, relief=SUNKEN)
        self.text = Text(self, font='Helvetica', bg='white', bd=1, width=width,
                         height=height)
        scroll = Scrollbar(self, bd=1, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        scroll.pack(side=RIGHT, expand=YES, fill=BOTH, padx=2, pady=2)

    def ajouter_texte(self, action_a_ecrire):
        """
        Écrit le message demandé dans la zone historique de coup et ramène la
        barre de défilement à la fin de l'historique
        """

        self.text.insert(END, action_a_ecrire + "\n")
        self.text.see("end")


class ScoreActuel(Label):
    def __init__(self, boss):
        Label.__init__(self, boss, font='Helvetica', text="score: ",
                       bg="white")

    def changer_score(self, score_a_ecrire):
        self.labelText = ('1.0', score_a_ecrire)


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

        self.geometry("250x250+550+250")  # 300x300 dimension+posX+posY
        self.resizable(width=0, height=0)  # empeche resize
        self.attributes('-topmost', 'true')
        Bouton(self, text="1 joueur", command=self.unjoueur).pack(pady=5,
                                                                  padx=10)
        Bouton(self, text="2 joueurs", command=self.deuxjoueurs).pack(pady=5,
                                                                      padx=10)

    def unjoueur(self):
        """ Donne la valeur 1 à self.nb_joueurs et ferme la fenêtre """

        self.nb_joueurs = 1
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def deuxjoueurs(self):
        """ Donne la valeur 2 à self.nb_joueurs et ferme la fenêtre """

        self.nb_joueurs = 2
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

        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
        Bouton(self, text="Normal", command=self.set_easy).pack(pady=15,
                                                                padx=10)
        Bouton(self, text="Difficile", command=self.set_hard).pack(pady=15,
                                                                   padx=10)
        Bouton(self, text="Légendaire", command=self.set_legend).pack(pady=15,
                                                                      padx=10)

    def set_easy(self):
        """ Donne la valeur 'Normal' à self.difficulte et ferme la fenêtre """

        self.difficulte = "Normal"
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def set_hard(self):
        """
        Donne la valeur 'Difficile' à self.difficulte et ferme la fenêtre
        """

        self.difficulte = "Difficile"
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def set_legend(self):
        """
        Donne la valeur 'Légendaire' à self.difficulte et ferme la fenêtre
        """

        self.difficulte = "Légendaire"
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

        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
        Bouton(self, text="Partie Classique", command=self.partie_classique).\
            pack(pady=5, padx=10)
        Bouton(self, text="Partie Personalisée", command=self.partie_perso).\
            pack(pady=5, padx=10)

    def partie_classique(self):
        """
        Donne la valeur 'classique' à self.type_partie et ferme la fenêtre
        """

        self.type_partie = 'classique'
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def partie_perso(self):
        """
        Donne la valeur 'perso' à self.type_partie et ferme la fenêtre
        """

        self.type_partie = 'perso'
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
        Label(self, text="Combien de cases?").pack(padx=20, pady=20, fill=X)
        self.gliss = Glissoir(self, orient=HORIZONTAL, relief=SUNKEN, bd=2,
                              from_=6, to_=12, tickinterval=2, resolution=2)
        self.gliss.pack(padx=20, pady=20, fill=X)
        Bouton(self, text="jouer", command=self.set_perso).\
            pack(padx=20, pady=20, fill=X)

    def set_perso(self):
        """
        Envoie les paramètres choisis par l'utilisateur et ferme la fenêtre
        """

        self.nb_cases = self.gliss.get()
        self.grab_release()
        self.master.focus_set()
        self.destroy()

# ====== Définition de la fenêtre maîtresse ====== #


class Brothello(Tk):
    """Classe de la fenêtre principale du jeu"""

    def __init__(self):
        """Constructeur de la fenêtre principale"""

        super().__init__()

        # Caractérisiques de la fenêtre principale

        self.title("Brothello")
        #Brothello.config(self, bg="white")
        self.geometry("800x650+550+250")
        self.resizable(height=0, width=0)
        bout_conseil = Bouton(self, text="Voir les coups possibles",
                              command=self.conseil, state=DISABLED)
        bout_conseil.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        bout_newgame = Bouton(self, text="Nouvelle partie",
                              command=self.nouvelle_partie, state=DISABLED)
        bout_newgame.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)
        bout_abandon = Bouton(self, text="Abandonner", command=self.abandon,
                              state=DISABLED)
        bout_abandon.grid(row=2, column=2, padx=5, pady=5, sticky=W+E)
        ScoreActuel(self).grid(row=0, column=2, sticky=W)
        self.histo = Historique(self, height=21)
        self.histo.grid(row=3, column=2, padx=10, pady=5, sticky=W+E)


        # Gestion couleur du board
        Bouton(self, text="Changer couleur",
               command=self.action_bouton_couleur) \
            .grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # Définition des caractéristiques de la partie par défaut
        self.nb_cases = 8
        self.difficulte = 'Normal'
        self.type_partie = 'perso'
        self.nb_joueurs = 1
        self.largeur = 500//self.nb_cases

        # Popups choix options du jeu
        try:
            fen_joueur = FenJoueurs(self)
            self.wait_window(fen_joueur)
            if fen_joueur.nb_joueurs not in [1, 2]:
                raise ErreurChoix("Erreur. Fin de la partie.")
            self.nb_joueurs = fen_joueur.nb_joueurs
            if self.nb_joueurs == 1:
                fen_diff = FenNiveauDif(self)
                self.wait_window(fen_diff)
                self.difficulte = fen_diff.difficulte
                if fen_diff.difficulte not in ['Normal', 'Difficile',
                                               'Légendaire']:
                    raise ErreurChoix("Erreur. Fin de la partie.")
                fen_type = FenTypePartie(self)
                self.wait_window(fen_type)
                if fen_type.type_partie not in ['classique', 'perso']:
                    raise ErreurChoix("Erreur. Fin de la partie.")
                self.type_partie = fen_type.type_partie
            elif self.nb_joueurs == 2:
                fen_type = FenTypePartie(self)
                self.wait_window(fen_type)
                if fen_type.type_partie not in ['classique', 'perso']:
                    raise ErreurChoix("Erreur. Fin de la partie.")
                self.type_partie = fen_type.type_partie
            else:
                fen_joueur = FenJoueurs(self)  # Si erreur nb_joueurs redemande
                self.wait_window(fen_joueur)
                if fen_joueur.nb_joueurs not in [1, 2]:
                    raise ErreurChoix("Erreur. Fin de la partie.")
                self.nb_joueurs = fen_joueur.nb_joueurs
            if self.type_partie == 'classique':
                self.nb_cases = 8
            elif self.type_partie == 'perso':
                fen_perso = FenPartiePerso(self)
                self.wait_window(fen_perso)
                self.nb_cases = fen_perso.nb_cases
            else:
                fen_perso = FenPartiePerso(self)  # Si erreur redemande
                self.wait_window(fen_perso)
                self.nb_cases = fen_perso.nb_cases

        except(ErreurChoix, AttributeError):
            box_fin = messagebox.askyesno('Erreur! Mauvaise réponse',
                                          'Erreur dans les réponses, voulez-'
                                          'vous recommencer?')
            if box_fin:
                self.nouvelle_partie()
            else:
                self.destroy()

        # Création du canevas
        self.fond()
        self.initialiser_damier()
        self.anciennes_pieces = {}

        # Création de l'instance du jeu et liste des coups possibles
        self.partie = Partie(self.nb_joueurs, self.difficulte, self.nb_cases)
        self.placer_pieces()

        # Activation des éléments de l'interface
        bout_newgame.config(state=NORMAL)
        bout_abandon.config(state=NORMAL)
        bout_conseil.config(state=NORMAL)

    def fond(self):
        self.can1 = Canvas(self, width = 800, height = 650)
        self.photo = PhotoImage(file="bois.gif")
        self.can1.create_image(400, 325, image=self.photo)
        self.can1.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)


    def action_bouton_couleur(self):
        """
        Permet de changer de couleur avec le selecteur de couleur, puis
        redessine le damier et les pieces en fonction de cette couleur
        """

        couleur.choisir_couleur()
        self.damier.dessiner_carres()
        self.placer_pieces()

    def initialiser_damier(self):
        """
        Crée le cavevas de la planche de jeu
        """

        self.largeur = 500//self.nb_cases
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=2, column=0, rowspan=3, padx=5, pady=5)
        self.damier.bind("<Button-1>", self.pointeur)
        self.damier.dessiner_carres()

    def placer_pieces(self):
        """Dessine les pieces nouvelles ou modifies"""

        for piece in self.partie.planche.cases:
            if piece not in self.anciennes_pieces:
                # Placer au centre de la case
                mid_x = piece[0] * self.largeur + self.largeur // 2
                mid_y = piece[1] * self.largeur + self.largeur // 2

                couleur_piece = self.partie.planche.cases[piece].couleur
                if couleur_piece == "blanc":
                    couleur_piece = "white"
                elif couleur_piece == "noir":
                    couleur_piece = "black"
                self.anciennes_pieces[piece] = self.partie.planche.cases[
                    piece].couleur
                self.dessiner_piece(mid_x, mid_y, couleur_piece)
                self.damier.update_idletasks()
                sleep(0.35)

        for piece in self.partie.planche.cases:
            if piece in self.anciennes_pieces:
                if self.partie.planche.cases[piece].couleur != \
                        self.anciennes_pieces[piece]:
                    # Placer au centre de la case
                    mid_x = piece[0] * self.largeur + self.largeur // 2
                    mid_y = piece[1] * self.largeur + self.largeur // 2

                    couleur_piece = self.partie.planche.cases[piece].couleur
                    if couleur_piece == "blanc":
                        couleur_piece = "white"
                    elif couleur_piece == "noir":
                        couleur_piece = "black"
                    self.anciennes_pieces[piece] = \
                        self.partie.planche.cases[piece].couleur
                    self.dessiner_piece(mid_x, mid_y, couleur_piece)
                    self.damier.update_idletasks()
                    sleep(0.35)

        for piece in self.partie.planche.cases:
            # Placer au centre de la case
            mid_x = piece[0] * self.largeur + self.largeur // 2
            mid_y = piece[1] * self.largeur + self.largeur // 2

            couleur_piece = self.partie.planche.cases[piece].couleur
            if couleur_piece == "blanc":
                couleur_piece = "white"
            elif couleur_piece == "noir":
                couleur_piece = "black"

            self.dessiner_piece(mid_x, mid_y, couleur_piece)

    def dessiner_piece(self, mid_x: int, mid_y: int, couleur_piece: str):
        """ Trace la pièce dans le canevas"""

        r = self.largeur // 5 * 2
        self.damier.create_oval(mid_x - r, mid_y - r, mid_x + r, mid_y + r,
                                fill=couleur_piece, outline='black')

    def tour_humain(self, case_clic: tuple):
        """ Joue le coup du clic humain """

        self.partie.tour(case_clic)
        ligne_jouee = chr(case_clic[0] + 64)
        col_jouee = str(case_clic[1] + 1)
        coup_jouer = ligne_jouee + col_jouee
        self.histo.ajouter_texte(f"Joueur {self.partie.joueur_courant.couleur}"
                                 f" a joué en {coup_jouer}")

    def pointeur(self, event: EventType):
        """
        Établie dans quelle case le joueur a cliqué, joue son coup ou lui dit
        si ce n'est pas possible et pourquoi. Envoie l'informations à Partie
        pour modifier les données. Effectue le changement de joueurs. Si ce
        joueur est un ordinateur, lui fait aussi joueur son tour avant
        d'attendre un nouveau clic

        :param event: Un clic sur le canevas de la planche de jeu
        """

        # coordonnées (x, y) de la case en range (0, nb_cases) ex (0, 4)
        case_clic = (event.x//self.largeur, event.y//self.largeur)
        ligne_jouee = chr(case_clic[0] + 64)
        col_jouee = str(case_clic[1] + 1)
        coup_jouer = ligne_jouee + col_jouee
        self.histo.ajouter_texte(f"Clic reçu en {coup_jouer}")

        # Valider puis jouer le coup
        if self.valider_coup(case_clic):
            self.tour_humain(case_clic)
            self.partie.jouer()
            self.placer_pieces()
            self.damier.update_idletasks()
            self.histo.update_idletasks()
            sleep(1)
            if self.partie.partie_terminee():
                self.histo.ajouter_texte(self.partie.determiner_gagnant())
                txt_fin = self.partie.determiner_gagnant() + \
                    '\nVoulez vous jouer une nouvelle partie?'
                box_fin = messagebox.showinfo('Partie teminée!', txt_fin)
                if not box_fin:
                    self.destroy()
                elif box_fin:
                    self.nouvelle_partie()

            self.histo.ajouter_texte("Tour du joueur {}".format(
                self.partie.couleur_joueur_courant))

            if self.partie.joueur_courant.obtenir_type_joueur() == \
                    'Ordinateur':
                self.tour_ordi()
                self.partie.jouer()
                self.placer_pieces()
                if self.partie.partie_terminee():
                    self.histo.ajouter_texte(self.partie.determiner_gagnant())
                    txt_fin = self.partie.determiner_gagnant() + \
                        '\nVoulez vous jouer une nouvelle partie?'
                    box_fin = messagebox.askyesno('Partie teminée!', txt_fin)
                    if box_fin:
                        self.nouvelle_partie()
                    else:
                        self.destroy()
                self.histo.ajouter_texte("Tour du joueur {}".format(
                    self.partie.couleur_joueur_courant))

    def tour_ordi(self):
        """ Fait jouer l'ordinateur """

        if self.partie.joueur_courant.obtenir_type_joueur() == 'Ordinateur':
            coup_ordi = self.partie.tour((-1, -1))
            ligne_jouee = chr(coup_ordi[0] + 64)
            col_jouee = str(coup_ordi[1] + 1)
            coup_jouer = ligne_jouee + col_jouee
            self.histo.ajouter_texte(
                f"Joueur {self.partie.joueur_courant.couleur}"
                f" a joué en {coup_jouer}")

    def valider_coup(self, position: tuple):
        """ Vérifie si coup valide, affiche msg sinon """
        msg=""
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

        if self.difficulte == "Normal":
            coups_possibles = self.partie.coups_possibles
            if not coups_possibles or len(coups_possibles) < 1:
                self.histo.ajouter_texte("Aucun coup possible!")
            for coup in coups_possibles:
                mid_x = coup[0] * self.largeur + self.largeur // 2
                mid_y = coup[1] * self.largeur + self.largeur // 2
                couleur_piece = 'light grey'
                self.dessiner_piece(mid_x, mid_y, couleur_piece)
                self.damier.update_idletasks()
                sleep(0.35)
            self.damier.dessiner_carres()
            self.placer_pieces()
            """

            self.dessiner_piece(mid_x, mid_y, couleur_piece)

    def dessiner_piece(self, mid_x: int, mid_y: int, couleur_piece: str):
         Trace la pièce dans le canevas

        r = self.largeur // 5 * 2
        self.damier.create_oval(mid_x - r, mid_y - r, mid_x + r, mid_y + r,
                                fill=couleur_piece)
                                """
        else:
            self.histo.ajouter_texte(" Aide seulement disponible en difficulté"
                                     " normale! Débrouillez-vous! ")


    def abandon(self):
        """
        Concède la victoire à l'ennemi et demande si le joueur souhaite jouer
        une autre partie
        """

        self.histo.ajouter_texte("Le joueur {} abandonne la partie! ".format(
            self.partie.couleur_joueur_courant))
        self.histo.ajouter_texte(self.partie.determiner_gagnant())
        txt_fin = (f"Joueur {self.partie.couleur_joueur_courant} "
                   f"abandonne la partie! \nVoulez vous jouer une nouvelle "
                   f"partie?")
        box_fin = messagebox.askyesno('Partie teminée!', txt_fin)
        if not box_fin:
            self.destroy()
        elif box_fin:
            self.nouvelle_partie()

    def nouvelle_partie(self):
        """ Démarre une nouvelle partie (Redémarre l'application) """

        self.destroy()
        le_jeu = Brothello()
        le_jeu.mainloop()


class ErreurChoix(Exception):
    """
    Classe d'erreur servant à attraper des données invalides lors des choix de
    l'utilisateur au début de la partie. Ou si celui-ci ferme les fenêtres
    TopLevel sans répondre
    """

    pass
