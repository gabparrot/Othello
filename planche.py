from othello.piece import Piece
import numpy as np


class Planche:
    """
    Classe représentant la planche d'un jeu d'Othello.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle planche.
        """
        # Dictionnaire de cases. La clé est une position (ligne, colonne),
        # et la valeur une instance de la classe Piece.
        self.cases = {}

        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()

        # On joue au Othello 8x8
        self.nb_cases = 8

        # Matrice de cases numpy
        matrice_cases = np.ones((self.nb_cases, self.nb_cases), int)

        # Liste des index de cases [(0,0), (0,1), etc]
        self.liste_cases = []
        for i in np.argwhere(matrice_cases == 1):
            self.liste_cases.append(tuple(i))

    def get_piece(self, position):
        """
        Récupère une pièce dans la planche.

        Args:
            position: La position où récupérer la pièce, un tuple de
            coordonnées matricielles (ligne, colonne).

        Returns:
            La pièce à cette position s'il y en a une, None autrement.
        """
        if position in self.cases:
            return self.cases[position]
        else:
            return None

    def position_valide(self, position):
        """
        Vérifie si une position est valide (chaque coordonnée doit être dans
        les bornes).

        Args:
            position: Un couple (ligne, colonne), tuple de deux éléments.

        Returns:
            True si la position est valide, False autrement
        """
        if position in self.liste_cases:
            return True
        else:
            return False

    def obtenir_positions_mangees(self, position, couleur):
        """
        Détermine quelles positions seront mangées si un coup de la couleur
        passée est joué à la position passée.

        ***RETOURNEZ SEULEMENT LA LISTE DES POSITIONS MANGÉES, NE FAITES PAS
        APPEL À piece.echange_couleur() ICI.***

        Ici, commencez par considérer que, pour la position évaluée, des pièces
        peuvent être mangées dans 8 directions distinctes représentant les 8
        cases qui entourent la position évaluée. Vous devez donc vérifier, pour
        chacune de ces directions, combien de pièces sont mangées et retourner
        une liste regroupant les pièces mangées dans toutes les directions.

        Ici, une direction représente une liste de 2 entiers pour la
        déplacement en x et y. Par exemple, pour la direction diagonale où en
        explore vers le bas et vers la droite, on utiliserait la liste [1, 1].
        De même, pour la direction gauche, on utiliserait la liste [-1, 0].
        Il y a donc un total de 8 directions, représentant les 8 positions
        auxquelles la position actuelle peut toucher.

        Pensez à faire appel à la fonction
        obtenir_positions_mangees_direction()

        Args:
            position: La position du coup à jouer.
            couleur: La couleur du coup à jouer.

        Returns:
            une liste contenant toutes les positions qui seraient mangées par
            le coup.
        """
        pieces_mangees = []
        directions = {"Nord": (0, 1), "Sud": (0, -1), "Est": (1, 0), "Ouest":
                      (-1, 0), "Nord-Est": (1, 1), "Nord-Ouest": (-1, 1),
                      "Sud-Est": (1, -1), "Sud-Ouest": (-1, -1)}

        for direction in directions.values():
            piece_mangees_par_direction = \
                self.obtenir_positions_mangees_direction(couleur, direction,
                                                         position)
            if len(piece_mangees_par_direction) > 0:
                for chaque_piece in piece_mangees_par_direction:
                    pieces_mangees.append(chaque_piece)

        if len(pieces_mangees) == 0:
            return []
        else:
            return pieces_mangees

    def obtenir_positions_mangees_direction(self, couleur, direction,
                                            position):
        """
        Détermine les positions qui seront mangées si un coup de couleur
        "couleur" est joué à la position "position",
        si on parcourt la planche dans une direction "direction".

        Pour une direction donnée, vous devez parcourir la planche de jeu dans
        la direction. Tant que votre déplacement
        vous mène sur une pièce de la couleur mangée, vous continuez de vous
        déplacer. Trois situations surviennent
        alors pour mettre un terme au parours dans la direction :

        1) Vous arrivez sur une case vide. Dans ce cas, aucune pièce n'est
        mangée.

        2) Vous arrivez sur une case extérieure à la planche. Encore une fois,
        aucune pièce n'est mangée.

        3) Vous arrivez sur une case de la même couleur que le coup initial.
        Toutes les pièces de la couleur opposée
        que vous avez alors rencontrées dans votre parcours doivent alors être
        ajoutées à grande liste des pièces
        mangées cumulées.

        N.B. : Cette méthode peut être implémentée par au moins deux techniques
         différentes alors laissez place à votre
        imagination et explorez ! Une méthode faisant une boucle d'exploration
        complète et une méthode de parcours
        récursif  sont quelques-unes des façons de faire que vous pouvez
        explorer. Il se peut même que votre solution
        ne soit pas dans les solutions énumérées précédemment.

        Args:
            couleur: La couleur du coup évalué
            direction: La direction de parcours évaluée
            position: La position du coup évalué

        Returns:
            La liste (peut-être vide) de toutes les positions mangées à partir
            du coup et de la direction donnés.
        """

        pieces_mangees = []
        avancer = lambda x, y: tuple(np.array(x) + np.array(y))
        position = avancer(position, direction)

        while self.position_valide(position):
            if self.get_piece(position):
                if self.get_piece(position).couleur == couleur:
                    return pieces_mangees
                else:
                    pieces_mangees.append(position)
                    position = avancer(position, direction)
            else:
                return []
        return []

    def coup_est_possible(self, position, couleur):
        """
        Détermine si un coup est possible. Un coup est possible si au moins une
        pièce est mangée par celui-ci. ET s'il n'y a pas déjà une pièce
        présente

        Args:
            position: La position du coup évalué
            couleur: La couleur du coup évalué

        Returns:
            True, si le coup est valide, False sinon
        """
        if not self.get_piece(position) and position in \
                self.lister_coups_possibles_de_couleur(couleur).keys():
            return True
        return False

    def lister_coups_possibles_de_couleur(self, couleur):
        """
        Fonction retournant la liste des coups possibles d'une certaine
        couleur. Un coup est considéré possible si au moins une pièce est
        mangée quand la couleur "couleur" joue à une certaine position, ne
        l'oubliez pas (et si cette case est vide)

        Args:
            couleur: La couleur ("blanc", "noir") des pièces dont on considère
            le déplacement, un string

        Returns:
            Un dictionnaire de positions de coups possibles pour la couleur
            "couleur"
        """

        pieces_mangees_par_coup = {}

        for case in self.liste_cases:
            if not self.get_piece(case):
                positions_mangees = self.obtenir_positions_mangees(case,
                                                                   couleur)
                if len(positions_mangees) > 0:
                    pieces_mangees_par_coup[case] = positions_mangees

        return pieces_mangees_par_coup

    def jouer_coup(self, position, couleur):
        """
        Joue une pièce de la couleur "couleur" à la position "position".

        Cette méthode doit également:
        - Ajouter la pièce aux pièces de la planche.
        - Faire les changements de couleur pour les pièces mangées par le coup.
        - Retourner un message indiquant "ok" ou "erreur".

        ATTENTION: Ne dupliquez pas de code! Vous savez déjà qu'un coup est
                   valide si au moins une pièce est mangée par celui-ci. Vous
                   avez une méthode qui fait exactement ce travail à
                   programmer !

        Args:
            position: La position du coup.
            couleur: La couleur du coup.

        Returns:
            "ok" si le déplacement a été effectué car il est valide,
            "erreur" autrement.
        """
        try:
            assert self.coup_est_possible(position, couleur)
            assert position not in self.cases.keys()
            self.cases[position] = Piece(couleur)
            pieces_mangees = self.obtenir_positions_mangees(position, couleur)
            if len(pieces_mangees) > 0:
                for chaque_piece in pieces_mangees:
                    self.cases[chaque_piece].echange_couleur()
                return "ok"
            else:
                raise AssertionError

        except AssertionError:
            return "erreur"

    def convertir_en_chaine(self):
        """
        Retourne une chaîne de caractères où chaque case est écrite sur une
        ligne distincte. Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder
        une planche dans un fichier.

        Returns:
            La chaîne de caractères.
        """
        pass
        # ligne = 0
        # colonne = 0
        # chaine = ""
        #
        # while ligne <= self.nb_cases in self.cases[(colonne, ligne)]:
        #     if colonne == self.nb_cases:
        #         colonne = 0
        #         ligne += 1
        #     else:
        #         chaine += colonne,",", ligne,",", Piece, "\n"
        #     colonne += 1
        #
        # return chaine

    def charger_dune_chaine(self, chaine):
        """
        Remplit la planche à partir d'une chaîne de caractères comportant
        l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Args:
            chaine: La chaîne de caractères, un string.
        """
        pass
        # a = 0
        # b = 0
        # c = 0
        #
        # while True:
        #     self.cases[(chaine[a], chaine[b])] = Piece(chaine[c])
        #     a += 3
        #     b += 3
        #     c += 3

    def initialiser_planche_par_default(self):
        """
        Initialise une planche de base avec la position initiale des pièces.
        """
        self.cases.clear()
        self.cases[(3, 3)] = Piece("blanc")
        self.cases[(3, 4)] = Piece("noir")
        self.cases[(4, 3)] = Piece("noir")
        self.cases[(4, 4)] = Piece("blanc")

    def __repr__(self):
        """
        Cette méthode spéciale permet de modifier le comportement d'une
        instance de la classe Planche pour l'affichage. Faire un
        print(une_planche) affichera la planche à l'écran.
        """
        s = "  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"

        for i in range(0, self.nb_cases):
            s += str(i)+" |   " if (i, 0) in self.cases else str(i) + " | "
            for j in range(0, self.nb_cases):
                if (i, j) in self.cases:
                    s += (str(self.cases[(i, j)]) + "  |   ")
                else:
                    s += "         |   "
            s += str(i)
            if i != self.nb_cases - 1:
                s += "\n  +---+---+---+---+---+---+---+---+\n"

        s += "\n  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"

        return s
