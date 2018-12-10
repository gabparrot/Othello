from othello.planche import Planche, IADifficile, IALegendaire, IANormale
from othello.joueur import JoueurOrdinateur, JoueurHumain


class Partie:
    """
     Définition de la classe Partie qui englobe la planche, l'IA, les pièces,
     les joueurs et détermine les coups possibles
    """

    def __init__(self, nb_joueurs: int, difficulte: str, nb_cases: int,
                 nom_fichier=None):
        """
        Méthode d'initialisation d'une partie. On initialise 4 membres:
        - planche: contient la planche de la partie, celui-ci contenant le
          dictionnaire de pièces.
        - couleur_joueur_courant: le joueur à qui c'est le tour de jouer.
        - tour_precedent_passe: un booléen représentant si le joueur précédent
          a passé son tour parce qu'il n'avait aucun coup disponible.
        - deux_tours_passes: un booléen représentant si deux tours ont été
          passés de suite, auquel cas la partie
           devra se terminer.
        - coups_possibles : une liste de tous les coups possibles en fonction
          de l'état actuel de la planche, initialement vide.
        - intelligenceartificielle: classe contenant les méthodes d'analyse de
          partie de l'IA

        On initialise ensuite les joueurs selon la paramètre nom_fichier. Si
        l'utilisateur a précisé un nom_fichier, on fait appel à la méthode
        self.charger() pour charger la partie à partir d'un fichier. Sinon, on
        fait appel à self.initialiser_joueurs(), qui va demander à
        l'utilisateur quels sont les types de joueurs qu'il désire.
        """

        self.difficulte = difficulte
        self.nb_cases = nb_cases
        self.planche = Planche(self.nb_cases)
        self.nb_joueurs = nb_joueurs

        self.couleur_joueur_courant = "noir"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

        self.coups_du_tour = self.planche.lister_coups_possibles_de_couleur(
                self.joueur_courant.couleur)
        self.coups_possibles = self.coups_du_tour[0]

    def initialiser_joueurs(self):
        """
        On initialise ici trois attributs : joueur_noir, joueur_blanc et
        joueur_courant (initialisé à joueur_noir).

        Pour créer les objets joueur, faites appel à demander_type_joueur()
        """

        self.joueur_noir = self.creer_joueur("Humain", "noir")
        if self.nb_joueurs == 1:
            self.joueur_blanc = self.creer_joueur("Ordinateur", "blanc")
        elif self.nb_joueurs == 2:
            self.joueur_blanc = self.creer_joueur("Huamin", "blanc")
        self.joueur_courant = self.joueur_noir

    @staticmethod
    def creer_joueur(typejoueur: str, couleur: str):
        """
        Crée l'objet Joueur approprié, selon le type passé en paramètre.

        Args:
            typejoueur: le type de joueur, "Ordinateur" ou "Humain"
            couleur: la couleur du pion joué par le jouer, "blanc" ou "noir"

        Returns:
            Un objet JoueurHumain si le type est "Humain", JoueurOrdinateur
            sinon
        """
        if typejoueur == "Ordinateur":
            joueur = JoueurOrdinateur(couleur)
        else:
            joueur = JoueurHumain(couleur)

        return joueur

    def tour(self, coup_clic: tuple):
        """
        Cette méthode simule le tour d'un joueur, et effectue les actions
         suivantes:
        - Si le joueur courant est un Ordinateur, lui demande le coup qu'il
          veut effecteur avec demander_coup()
        - S'il s'agit d'un joueur humain, utilise le paramètre coup_clic pour
          effectuer son coup sur la planche
        - Joue le coup sur la planche de jeu, avec la bonne couleur.

        :param coup_clic: tuple de la position cliquée par le joueur sur le GUI

        :returns: La position jouée par le joueur
        """
        if self.joueur_courant.obtenir_type_joueur() == "Humain":
            coup_demander = coup_clic
            self.planche.jouer_coup(coup_demander,
                                    self.joueur_courant.couleur)
        else:
            coup_demander = self.demander_coup((-1, -1))
            self.planche.jouer_coup(coup_demander,
                                    "blanc")
        return coup_demander

    def demander_coup(self, coup_clic: tuple):
        """
        Demande au joueur courant le coup qu'il souhaite jouer. Si le joueur
        courant est un humain, on appelle directement
        self.joueur_courant.choisir_coup() pour ce faire. S'il s'agit d'un
        ordinateur, on commence par filtrer les meilleurs coups avec
        self.intelligenceartificielle.filtrer_meilleurs_coups() avant de faire
        choisir coup.

        :returns coup_choisi: un couple positionnel sous forme de tuple
            représentant le coup demandé par le joueur.
        """

        if self.joueur_courant.obtenir_type_joueur() == "Humain":
            coup_choisi = coup_clic
        else:
            if self.difficulte == "Légendaire":
                self.intelligenceartificielle = IALegendaire(
                    self.planche.nb_cases, self.planche.cases,
                    self.couleur_joueur_courant)
            elif self.difficulte == "Difficile":
                self.intelligenceartificielle = IADifficile(
                    self.planche.nb_cases, self.planche.cases,
                    self.couleur_joueur_courant)
            else:
                self.intelligenceartificielle = IANormale(
                    self.planche.nb_cases, self.planche.cases,
                    self.couleur_joueur_courant)
            coups_ia = self.intelligenceartificielle.\
                filtrer_meilleurs_coups()
            coup_choisi = self.joueur_courant.choisir_coup(coups_ia)
        return coup_choisi

    def partie_terminee(self):
        """
        Détermine si la partie est terminée, Une partie est terminée si toutes
        les cases de la planche sont remplies ou si deux tours consécutifs ont
        été passés.

        :returns: True si terminée, False sinon
        """

        if self.deux_tours_passes:
            return True
        elif len(self.planche.cases) == self.planche.nb_cases ** 2:
            return True
        else:
            return False

    def determiner_gagnant(self):
        """
        Détermine le gagnant de la partie. Le gagnant est simplement la couleur
        pour laquelle il y a le plus de pions sur la planche de jeu.

        :returns msg: Message contenant les informations sur le gagnant, ou de
            partie nulle
        """

        pieces_noires = 0
        pieces_blanches = 0

        for case in self.planche.liste_cases:
            if self.planche.get_piece(case):
                if self.planche.get_piece(case).couleur == "blanc":
                    pieces_blanches += 1
                elif self.planche.get_piece(case).couleur == "noir":
                    pieces_noires += 1

        if pieces_noires > pieces_blanches:
            gagnant = self.joueur_noir
        elif pieces_noires < pieces_blanches:
            gagnant = self.joueur_blanc
        else:
            gagnant = None

        if gagnant:
            msg = "La partie est terminée, le joueur {} l'emporte {} à {}".\
                format(gagnant.couleur, max(pieces_noires, pieces_blanches),
                       min(pieces_noires, pieces_blanches))
            return msg
        else:
            msg = "Partie nulle! Les deux joueurs terminent avec un score"
            "de {}".format(pieces_noires)  # noir ou blanc même chose
            return msg

    def jouer(self):
        """
        Effectue les opérations de fin de tour:

        - Effectue le changement de joueur. Modifie à la fois les attributs
            self.joueur_courant et self.couleur_joueur_courant.

        - Détermine les coups possibles pour le joueur actuel.
        """

        if len(self.coups_possibles) < 1:
            if not self.tour_precedent_passe:
                self.tour_precedent_passe = True
            else:
                self.deux_tours_passes = True
        else:
            self.tour_precedent_passe = False
        if self.couleur_joueur_courant == "noir":
            self.joueur_courant = self.joueur_blanc
            self.couleur_joueur_courant = "blanc"
        else:
            self.joueur_courant = self.joueur_noir
            self.couleur_joueur_courant = "noir"

        self.coups_du_tour = self.planche.lister_coups_possibles_de_couleur(
                self.joueur_courant.couleur)
        self.coups_possibles = self.coups_du_tour[0]
