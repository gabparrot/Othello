from othello.piece import Piece
import numpy as np


class Planche:
    """
    Classe représentant la planche d'un jeu d'Othello.
    """

    def __init__(self, nb_cases: int):
        """
        Méthode spéciale initialisant une nouvelle planche.
        """

        # Dictionnaire de cases. La clé est une position (ligne, colonne),
        # et la valeur une instance de la classe Piece.
        self.cases = {}
        # Nombre de cases de large du damier
        self.nb_cases = nb_cases
        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()
        # Liste des coups pour la couleur courante
        self.coups_possibles = []

        # Matrice de cases numpy
        matrice_cases = np.ones((self.nb_cases, self.nb_cases), int)

        # Liste des index de cases [(0,0), (0,1), etc]
        self.liste_cases = []
        for i in np.argwhere(matrice_cases == 1):
            self.liste_cases.append(tuple(i))

    def get_piece(self, position: tuple):
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

    def position_valide(self, position: tuple):
        """
        Vérifie si une position est valide.

        Args:
            position: Un couple (ligne, colonne), tuple de deux éléments.

        Returns:
            True si la position est valide, False autrement.
        """

        if position in self.liste_cases:
            return True
        else:
            return False

    def obtenir_positions_mangees(self, position: tuple, couleur: str):
        """
        Détermine quelles positions seront mangées si un coup de la couleur
        passée est joué à la position passée.

        Args:
            position: La position du coup à jouer
            couleur: La couleur du coup à jouer

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

    def obtenir_positions_mangees_direction(self, couleur: str,
                                            direction: tuple, position: tuple):
        """
        Détermine les positions qui seront mangées si un coup de couleur
        "couleur" est joué à la position "position",
        si on parcourt la planche dans une direction "direction".

        Args:
            couleur: La couleur du coup évalué
            direction: La direction de parcours évaluée
            position: La position du coup évalué

        Returns:
            La liste (peut-être vide) de toutes les positions mangées à partir
            du coup et de la direction donnés.
        """

        pieces_mangees = []

        position = tuple(np.array(position) + np.array(direction))

        while self.position_valide(position):
            if self.get_piece(position):
                if self.get_piece(position).couleur == couleur:
                    return pieces_mangees
                else:
                    pieces_mangees.append(position)
                    position = tuple(np.array(position) + np.array(direction))
            else:
                return []
        return []

    def lister_coups_possibles_de_couleur(self, couleur: str):
        """
        Fonction établissant, pour chaque case, si le joueur courant peut
        jouer une pièce ou non, et sinon, si c'est parce qu'il y a déjà une
        pièce présente ou alors si c'est parce qu'aucune pièce ne serait mangée
        Args:
            couleur: La couleur ("blanc", "noir") des pièces dont on considère
                le déplacement, un string.

        Returns: tuple: tuple contenant la liste, pour le joueur courant, des
                coups possibles, la liste des coups impossibles car une pièce
                est présente, et la liste coups impossibles car aucune pièce
                ne serait mangée
        """

        self.coups_possibles = []
        self.impossible_piece_la = []
        self.impossible_zero_mangee = []

        for case in self.liste_cases:
            if self.get_piece(case):
                self.impossible_piece_la.append(case)
                continue
            positions_mangees = self.obtenir_positions_mangees(case,
                                                               couleur)
            if len(positions_mangees) > 0:
                self.coups_possibles.append(case)
            else:
                self.impossible_zero_mangee.append(case)

        return self.coups_possibles, self.impossible_piece_la, \
            self.impossible_zero_mangee

    def jouer_coup(self, position: tuple, couleur: str):
        """
        Joue une pièce de la couleur "couleur" à la position "position".

        - Ajoute la pièce aux pièces de la planche.
        - Fait les changements de couleur pour les pièces mangées par le coup.

        Args:
            position: La position du coup.
            couleur: La couleur du coup.
        """

        pieces_mangees = self.obtenir_positions_mangees(position, couleur)
        self.cases[position] = Piece(couleur)
        if len(pieces_mangees) > 0:
            for chaque_piece in pieces_mangees:
                self.cases[chaque_piece].echange_couleur()

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

        chaine_planche = ""

        for piece in self.cases:
            chaine_planche = chaine_planche + str(piece[0]) + "," + str(
                piece[1]) + "," + self.cases[piece].couleur + "\n"

        return chaine_planche

    def charger_dune_chaine(self, chaine: str):
        """
        Remplit la planche à partir d'une chaîne de caractères comportant
        l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Args:
            chaine: La chaîne de caractères, un string.
        """

        chaine = chaine.replace("\n", ",")
        chaine = chaine.split(",")

        x = 0

        self.cases.clear()

        while x in range(len(chaine) - 1):
            position = (int(chaine[x]), int(chaine[x + 1]))
            self.cases[position] = Piece(chaine[x + 2])

            x += 3

    def initialiser_planche_par_default(self):
        """
        Initialise une planche de base avec la position initiale des pièces.
        """
        mid = self.nb_cases // 2

        self.cases.clear()
        self.cases[mid-1, mid-1] = Piece("blanc")
        self.cases[(mid-1, mid)] = Piece("noir")
        self.cases[(mid, mid-1)] = Piece("noir")
        self.cases[(mid, mid)] = Piece("blanc")


class IANormale(Planche):
    """
    Classe représentant l'intelligence artificielle de l'ordinateur et
    possédant des méthodes de tris pour déterminer les meilleurs coups
    possibles, de niveau de difficulté légendaire
    """

    def __init__(self, nb_cases: int, dict_pieces: dict, couleur_courant: str):
        """Constructeur de IANormale, hérite de Planche """

        super(Planche, self).__init__()
        self.cases = dict_pieces
        self.nb_cases = nb_cases
        self.couleur = couleur_courant
        # Matrice de cases numpy
        matrice_cases = np.ones((self.nb_cases, self.nb_cases), int)

        # Liste des index de cases [(0,0), (0,1), etc]
        self.liste_cases = []
        for i in np.argwhere(matrice_cases == 1):
            self.liste_cases.append(tuple(i))
        self.coups_du_tour = self.lister_coups_possibles_de_couleur(
            couleur_courant)
        self.coups_possibles = self.coups_du_tour[0]

    def filtrer_meilleurs_coups(self):
        """Retourne le ou les coups mangeant le plus de pièces"""
        return self.coup_mange_le_plus(self.coups_possibles)

    def coup_mange_le_plus(self, coups_a_verifier: list):
        """
        Trouve le ou les coups qui mangent le plus de pièces ennemies et en
        retourne la liste.

        :param coups_a_verifier: liste des coups à vérifier

        :return: liste du ou des coups mangeant le plus de pièces
        """

        coups_qui_mangent_le_plus = []
        max_pieces_mangees = 0

        for coup in coups_a_verifier:
            position_mangees = self.obtenir_positions_mangees(coup,
                                                              self.couleur)
            if len(position_mangees) > max_pieces_mangees:
                coups_qui_mangent_le_plus.append(coup)
                max_pieces_mangees = len(position_mangees)
            elif len(position_mangees) == max_pieces_mangees:
                coups_qui_mangent_le_plus.append(coup)

        return coups_qui_mangent_le_plus


class IADifficile(Planche):
    """
    Classe représentant l'intelligence artificielle de l'ordinateur et
    possédant des méthodes de tris pour déterminer les meilleurs coups
    possibles, de niveau de difficulté légendaire
    """

    def __init__(self, nb_cases: int, dict_pieces: dict, couleur_courant: str):
        """ Constructeur de IADiffcile, hérite de Planche """

        super(Planche, self).__init__()
        self.cases = dict_pieces
        self.nb_cases = nb_cases
        self.couleur = couleur_courant
        # Matrice de cases numpy
        matrice_cases = np.ones((self.nb_cases, self.nb_cases), int)

        # Liste des index de cases [(0,0), (0,1), etc]
        self.liste_cases = []
        for i in np.argwhere(matrice_cases == 1):
            self.liste_cases.append(tuple(i))
        self.coups_du_tour = self.lister_coups_possibles_de_couleur(
            couleur_courant)
        self.coups_possibles = self.coups_du_tour[0]

    def filtrer_meilleurs_coups(self):
        """
        Prend la liste des coups possibles et retourne une liste contenant le
        ou les meilleurs coups dans une liste de tuple positionnels selon la
        stratégie de contrôle des coins suivante, dans cet ordre de priorités:

        1- Les coins;
        2- Les cases à 2 cases des coins, en lignes droite;
        3- Les cases à 2 cases des coins, en diagonale;

        Nous retournons une liste contenant le meilleur coup s'il n'y en a
        qu'un, ou la liste de tous les meilleurs coups égaux

        :return: liste de tuples représentant le ou les meilleurs coups à jouer
        """

        # à chaque priorité on append au lieu de return direct car AI grossira

        # Priorité 1: si on peut jouer des coins, en retourner la liste
        if self.verifier_priorite_1(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_1(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 2: Si aucun en priorité 1, refaire avec 2, et ainsi de suite
        if self.verifier_priorite_2(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_2(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 3:
        if self.verifier_priorite_3(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_3(
                self.coups_possibles)
            return coups_les_plus_forts
        return self.coups_possibles

    def verifier_priorite_1(self, coups_a_verifier: list):
        """
        Permet de vérifier si l'IA peut jouer des coups sur les coins de la
        planche. Si plusieurs coups aux coins sont possibles, elle tente de
        trouver le meilleur coup en appelant tri_vs_ennemi(), puis s'il en
        reste toujours plusieurs, en appelant limiter_degats(). Elle retourne
        le meilleur coup ou les meilleurs coups égaux dans une liste. S'il n'y
        en a aucun, elle retourne None

        :param coups_a_verifier: liste des coups possibles

        :return: le ou les coups aux coins, None sinon
        """

        coins = [(0, 0), (0, self.nb_cases-1), (self.nb_cases-1, 0),
                 (self.nb_cases-1, self.nb_cases-1)]
        coups_coins = []
        for coup in coups_a_verifier:
            if coup in coins:
                coups_coins.append(coup)

        if len(coups_coins) > 0:
            return coups_coins

        else:
            return None

    def verifier_priorite_2(self, coups_a_verifier: list):
        """
        Permet de verifier si l'IA peut jouer des coups à 2 cases des coins de
        la planche, en ligne droite de ceux-ci. Si oui, en retourne la liste,
        sinon, return None

        :param coups_a_verifier: liste des coups à verifier

        :return: liste des coups correspondants, None si aucun
        """

        deux_cases_du_coin_en_ligne = [(0, 2), (2, 0), (0, self.nb_cases-3),
                                       (2, self.nb_cases-1),
                                       (self.nb_cases-3, 0),
                                       (self.nb_cases-1, 2),
                                       (self.nb_cases-3, self.nb_cases-1),
                                       (self.nb_cases-1, self.nb_cases-3)]
        coups_prio_2 = []

        for coup in coups_a_verifier:
            if coup in deux_cases_du_coin_en_ligne:
                coups_prio_2.append(coup)

        if len(coups_prio_2) > 0:
            return coups_prio_2
        else:
            return None

    def verifier_priorite_3(self, coups_a_verifier: list):
        """
        Permet de verifier si l'IA peut jouer des coups à 2 cases des coins de
        la planche, en diagonale de ceux-ci. Si oui, en retourne la liste,
        sinon, return None

        :param coups_a_verifier: liste des coups à verifier

        :return: liste des coups correspondants, None si aucun
        """
        deux_cases_du_coin_en_diago = [(2, 2), (2, self.nb_cases - 3),
                                       (self.nb_cases - 3, 2),
                                       (self.nb_cases - 3, self.nb_cases - 3)]
        coups_prio_3 = []
        for coup in coups_a_verifier:
            if coup in deux_cases_du_coin_en_diago:
                coups_prio_3.append(coup)

        if len(coups_prio_3) > 0:
            return coups_prio_3
        else:
            return None


class IALegendaire(Planche):
    """
    Classe représentant l'intelligence artificielle de l'ordinateur et
    possédant des méthodes de tris pour déterminer les meilleurs coups
    possibles, de niveau de difficulté légendaire
    """

    def __init__(self, nb_cases: int, dict_pieces: dict, couleur_courant: str):
        """ Constructeur de IALegendaire, hérite de Planche """

        super(Planche, self).__init__()
        self.cases = dict_pieces
        self.nb_cases = nb_cases
        self.couleur = couleur_courant
        # Matrice de cases numpy
        matrice_cases = np.ones((self.nb_cases, self.nb_cases), int)

        # Liste des index de cases [(0,0), (0,1), etc]
        self.liste_cases = []
        for i in np.argwhere(matrice_cases == 1):
            self.liste_cases.append(tuple(i))
        self.coups_du_tour = self.lister_coups_possibles_de_couleur(
            couleur_courant)
        self.coups_possibles = self.coups_du_tour[0]

    def filtrer_meilleurs_coups(self):
        """
        Prend la liste des coups possibles et retourne une liste contenant le
        ou les meilleurs coups dans une liste de tuple positionnels selon la
        stratégie de contrôle des coins suivante, dans cet ordre de priorités:

        1- Les coins;
        2- Les cases à 2 cases des coins, en lignes droite;
        3- Les cases à 2 cases des coins, en diagonale;
        4- Les cases qui bordent les côtés de la planche;
        5- Les coups qui mangent le plus de pièces;
        Nous retournons une liste contenant le meilleur coup s'il n'y en a
        qu'un, ou la liste de tous les meilleurs coups égaux

        :return: liste de tuples représentant le ou les meilleurs coups à jouer
        """

        # à chaque priorité on append au lieu de return direct car AI grossira

        # Priorité 1: si on peut jouer des coins, en retourner la liste
        if self.verifier_priorite_1(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_1(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 2: Si aucun en priorité 1, refaire avec 2, et ainsi de suite
        if self.verifier_priorite_2(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_2(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 3:
        if self.verifier_priorite_3(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_3(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 4:
        if self.verifier_priorite_4(self.coups_possibles):
            coups_les_plus_forts = self.verifier_priorite_4(
                self.coups_possibles)
            return coups_les_plus_forts

        # Priorité 5:
        coups_les_plus_forts = self.verifier_priorite_5(self.coups_possibles)

        return coups_les_plus_forts

    def verifier_priorite_1(self, coups_a_verifier: list):
        """
        Permet de vérifier si l'IA peut jouer des coups sur les coins de la
        planche. Si plusieurs coups aux coins sont possibles, elle tente de
        trouver le meilleur coup en appelant tri_vs_ennemi(), puis s'il en
        reste toujours plusieurs, en appelant limiter_degats(). Elle retourne
        le meilleur coup ou les meilleurs coups égaux dans une liste. S'il n'y
        en a aucun, elle retourne None

        :param coups_a_verifier: liste des coups possibles

        :return: le ou les coups aux coins, None sinon
        """

        coins = [(0, 0), (0, self.nb_cases-1), (self.nb_cases-1, 0),
                 (self.nb_cases-1, self.nb_cases-1)]
        coups_coins = []

        for coup in coups_a_verifier:
            if coup in coins:
                coups_coins.append(coup)

        if len(coups_coins) > 0:
            return coups_coins
        else:
            return None

    def verifier_priorite_2(self, coups_a_verifier: list):
        """
        Permet de verifier si l'IA peut jouer des coups à 2 cases des coins de
        la planche, en ligne droite de ceux-ci. Si oui, en retourne la liste,
        sinon, return None

        :param coups_a_verifier: liste des coups à verifier

        :return: liste des coups correspondants, None si aucun
        """

        deux_cases_du_coin_en_ligne = [(0, 2), (2, 0), (0, self.nb_cases-3),
                                       (2, self.nb_cases-1),
                                       (self.nb_cases-3, 0),
                                       (self.nb_cases-1, 2),
                                       (self.nb_cases-3, self.nb_cases-1),
                                       (self.nb_cases-1, self.nb_cases-3)]
        coups_prio_2 = []

        for coup in coups_a_verifier:
            if coup in deux_cases_du_coin_en_ligne:
                coups_prio_2.append(coup)

        if len(coups_prio_2) > 0:
            return coups_prio_2
        else:
            return None

    def verifier_priorite_3(self, coups_a_verifier: list):
        """
        Permet de verifier si l'IA peut jouer des coups à 2 cases des coins de
        la planche, en diagonale de ceux-ci. Si oui, en retourne la liste,
        sinon, return None

        :param coups_a_verifier: liste des coups à verifier

        :return: liste des coups correspondants, None si aucun
        """

        deux_cases_du_coin_en_diago = [(2, 2), (2, self.nb_cases - 3),
                                       (self.nb_cases - 3, 2),
                                       (self.nb_cases - 3, self.nb_cases - 3)]
        coups_prio_3 = []

        for coup in coups_a_verifier:
            if coup in deux_cases_du_coin_en_diago:
                coups_prio_3.append(coup)

        if len(coups_prio_3) > 0:
            return coups_prio_3
        else:
            return None

    def verifier_priorite_4(self, coups_a_verifier: list):
        """
        Permet de verifier si l'IA peut jouer des coups sur les bordures de
        la planche, excluant les cases en contact avec les coins, afin d'éviter
        que le joueur adverse puisse jouer aux coins au prochain tour.

        :param coups_a_verifier: liste des coups à verifier

        :return: liste des coups correspondants, None si aucun
        """

        cases_bordures = []

        for i in range(self.nb_cases):
            if i == 0 or i == self.nb_cases-1:
                for j in range(3, self.nb_cases - 3):
                    cases_bordures.append((i, j))
            else:
                if i in range(3, self.nb_cases - 3):
                    for j in range(self.nb_cases):
                        if j == 0 or j == self.nb_cases-1:
                            cases_bordures.append((i, j))

        coups_prio_4 = []

        for coup in coups_a_verifier:
            if coup in cases_bordures:
                coups_prio_4.append(coup)

        if len(coups_prio_4) > 0:
            return coups_prio_4
        else:
            return None

    def verifier_priorite_5(self, coups_a_verifier: list):
        """
        Trouve le ou les coups qui mangent le plus de pièces ennemies et en
        retourne la liste.

        :param coups_a_verifier: liste des coups à vérifier

        :return: liste du ou des coups mangeant le plus de pièces
        """

        coups_qui_mangent_le_plus = []
        max_pieces_mangees = 0

        for coup in coups_a_verifier:
            position_mangees = self.obtenir_positions_mangees(coup,
                                                              self.couleur)
            if len(position_mangees) > max_pieces_mangees:
                coups_qui_mangent_le_plus.append(coup)
                max_pieces_mangees = len(position_mangees)
            elif len(position_mangees) == max_pieces_mangees:
                coups_qui_mangent_le_plus.append(coup)

        return coups_qui_mangent_le_plus
