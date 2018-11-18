from othello.planche import Planche
from othello.joueur import JoueurOrdinateur, JoueurHumain


class Partie:
    def __init__(self, nom_fichier=None):
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

        On initialise ensuite les joueurs selon la paramètre nom_fichier. Si
        l'utilisateur a précisé un nom_fichier, on fait appel à la méthode
        self.charger() pour charger la partie à partir d'un fichier. Sinon, on
        fait appel à self.initialiser_joueurs(), qui va demander à
        l'utilisateur quels sont les types de joueurs qu'il désire.
        """
        self.planche = Planche()

        self.couleur_joueur_courant = "noir"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []

        self.pieces_mangees_par_coup_possible = {}

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

    def initialiser_joueurs(self):
        """
        On initialise ici trois attributs : joueur_noir, joueur_blanc et
        joueur_courant (initialisé à joueur_noir).

        Pour créer les objets joueur, faites appel à demander_type_joueur()
        """

        self.joueur_noir = self.demander_type_joueur("noir")
        self.joueur_blanc = self.demander_type_joueur("blanc")
        self.joueur_courant = self.joueur_noir

    def demander_type_joueur(self, couleur):
        """
        Demande à l'usager quel type de joueur ('Humain' ou 'Ordinateur') il
        désire pour le joueur de la couleur.

        Tant que l'entrée n'est pas valide, on continue de demander à
        l'utilisateur.

        Faites appel à self.creer_joueur() pour créer le joueur lorsque
        vous aurez le type.

        Args:
            couleur: La couleur pour laquelle on veut le type de joueur.

        Returns:
            Un objet Joueur, de type JoueurHumain si l'usager a entré 'Humain',
            JoueurOrdinateur s'il a entré
            'Ordinateur'.
        """
        type_joueur = ""
        types_joueurs = ("Humain", "Ordinateur")

        while type_joueur not in types_joueurs:         # variable haut de page
            type_joueur = input("Est-ce que le joueur {} sera un Humain ou"
                                " un Ordinateur? ".format(couleur)).title()
            if type_joueur not in types_joueurs:
                print("Erreur, type invalide, veuillez réessayer.")
            else:
                return self.creer_joueur(type_joueur, couleur)

    def creer_joueur(self, type, couleur):
        """
        Crée l'objet Joueur approprié, selon le type passé en paramètre.

        Pour créer les objets, vous n'avez qu'à faire appel à leurs
        constructeurs, c'est-à-dire à JoueurHumain(couleur), par exemple.

        Args:
            type: le type de joueur, "Ordinateur" ou "Humain"
            couleur: la couleur du pion joué par le jouer, "blanc" ou "noir"

        Returns:
            Un objet JoueurHumain si le type est "Humain", JoueurOrdinateur
            sinon
        """
        if type == "Ordinateur":
            joueur = JoueurOrdinateur(couleur)
        else:
            joueur = JoueurHumain(couleur)

        return joueur

    def valider_position_coup(self, position_coup):
        """
        Vérifie la validité de la position désirée pour le coup. On retourne un
        message d'erreur approprié pour chacune des trois situations suivantes:

        1) Le coup tenté ne représente pas une position valide de la planche de
           jeu.

        2) Une pièce se trouve déjà à la position souhaitée.

        3) Le coup ne fait pas partie de la liste des coups valides.

        ATTENTION: Utilisez les méthodes et attributs de self.planche ainsi que
                   la liste self.coups_possibles pour connaître les
                   informations nécessaires.
        ATTENTION: Bien que cette méthode valide plusieurs choses, les méthodes
                   programmées dans la planche vous simplifieront la tâche!

        Args:
            position_coup: La position du coup à valider.

        Returns:
            Un couple où le premier élément représente la validité de la
            position (True ou False), et le
            deuxième élément est un éventuel message d'erreur.
        """
        if position_coup == "erreur":
            print("Une erreur s'est produite, assurez vous d'entre un chiffre "
                  "entre 0 et 7 et qu'une pièce soit mangée. "
                  "Veuillez recommencez. ")
        if not self.planche.position_valide(position_coup):
            return (False, "Position ne respecte pas les bornes de la planche."
                    " Veuillez recommencer. ")
        elif position_coup not in self.coups_possibles:
            if self.planche.get_piece(position_coup):
                return (False, "Coup impossible. Il y a déjà une pièce à cette"
                               " position. Veuillez recommencer. ")
            return (False, "Coup impossible car aucune pièce ne serait "
                           "mangée! Veuillez recommencer. ")
        else:
            return True, "Coup accepté. "

    def tour(self):
        """
        Cette méthode simule le tour d'un joueur, et doit effectuer les actions
         suivantes:
        - Demander la position du coup au joueur courant. Tant que la position
          n'est pas validée, on continue de demander. Si la position est
          invalide, on affiche le message d'erreur correspondant. Pour demander
          la position, faites appel à la fonction choisir_coup de l'attribut
          self.joueur_courant, à laquelle vous devez passer la liste de coups
          possibles. Pour valider le coup retourné, pensez à la méthode de
          validation de coup que vous avez déjà à implémenter.
        - Jouer le coup sur la planche de jeu, avec la bonne couleur.
        - Si le résultat du coup est "erreur", afficher un message d'erreur.

        ***Vous disposez d'une méthode pour demander le coup à l'usager dans
        cette classe et la classe planche
        possède à son tour une méthode pour jouer un coup, utilisez-les !***
        """
        coup_fait = False
        coup_demander = self.joueur_courant.choisir_coup(
                self.pieces_mangees_par_coup_possible)

        # Tant que coup est invalide on affiche msg erreur et redemande
        while not coup_fait:
            if not self.valider_position_coup(coup_demander)[0]:
                print(self.valider_position_coup(coup_demander)[1])
                coup_demander = self.joueur_courant.choisir_coup(
                    self.pieces_mangees_par_coup_possible)
                continue
            else:
                coup_fait = True

        print(self.planche.jouer_coup(coup_demander,
                                      self.couleur_joueur_courant))

    def passer_tour(self):
        """
        Affiche un message indiquant que le joueur de la couleur courante ne
        peut jouer avec l'état actuel de la
        planche et qu'il doit donc passer son tour.
        """
        print("Aucun coup possible, joueur {} passe son tour".format(
                  self.couleur_joueur_courant))

    def partie_terminee(self):
        """
        Détermine si la partie est terminée, Une partie est terminée si toutes
        les cases de la planche sont remplies ou si deux tours consécutifs ont
        été passés (pensez à l'attribut self.deux_tours_passes).
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

        Affichez un message indiquant la couleur gagnante ainsi que le nombre
        de pièces de sa couleur ou encore un message annonçant un match nul,
        le cas échéant.
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
            print("La partie est terminée, le joueur {} l'emporte {} à {}"
                  .format(gagnant.couleur, max(pieces_noires, pieces_blanches),
                          min(pieces_noires, pieces_blanches)))
        else:
            print("Partie nulle! Les deux joueurs terminent avec un score "
                  "de {}".format(pieces_noires))  # noir ou blanc même chose

    def jouer(self):
        """
        Démarre une partie. Tant que la partie n'est pas terminée, on fait les
        choses suivantes :

        1) On affiche la planche de jeu ainsi qu'un message indiquant à quelle
           couleur c'est le tour de jouer. Pour afficher une planche, faites
           appel à print(self.planche)

        2) On détermine les coups possibles pour le joueur actuel. Pensez à
          utiliser une fonction que vous avez à
           implémenter pour Planche, et à entreposer les coups possibles dans
           un attribut approprié de la partie.

        3) Faire appel à tour() ou à passer_tour(), en fonction du nombre de
            coups disponibles pour le joueur actuel.
           Mettez aussi à jour les attributs self.tour_precedent_passe et
           self.deux_tours_passes.

        4) Effectuer le changement de joueur. Modifiez à la fois les attributs
            self.joueur_courant et
           self.couleur_joueur_courant.

        5) Lorsque la partie est terminée, afficher un message mentionnant le
            résultat de la partie. Vous avez une
           fonction à implémenter que vous pourriez tout simplement appeler.
        """

        while not self.partie_terminee():
            print(self.planche)
            self.pieces_mangees_par_coup_possible.clear()
            self.pieces_mangees_par_coup_possible = \
                self.planche.lister_coups_possibles_de_couleur(
                    self.joueur_courant.couleur)
            print(self.joueur_courant.couleur)
            self.coups_possibles = list(
                self.pieces_mangees_par_coup_possible.keys())
            if len(self.pieces_mangees_par_coup_possible) < 1:
                self.passer_tour()
                if not self.tour_precedent_passe:
                    self.tour_precedent_passe = True
                else:
                    self.tour_precedent_passe = True
                    self.deux_tours_passes = True
                    self.partie_terminee()
            else:
                self.tour()
                if self.couleur_joueur_courant == "noir":
                    self.joueur_courant = self.joueur_blanc
                    self.couleur_joueur_courant = "blanc"
                else:
                    self.joueur_courant = self.joueur_noir
                    self.couleur_joueur_courant = "noir"
                self.tour_precedent_passe = False

        print(self.planche)
        self.determiner_gagnant()

    def sauvegarder(self, nom_fichier):
        """
        Sauvegarde une partie dans un fichier. Le fichier condiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le tour précédent a été passé.
        - Une ligne contenant True ou False, si les deux derniers tours ont été
          passés.
        - Une ligne contenant le type du joueur blanc.
        - Une ligne contenant le type du joueur noir.
        - Le reste des lignes correspondant à la planche. Voir la méthode
          convertir_en_chaine de la planche
         pour le format.

        ATTENTION : L'ORDRE DES PARAMÈTRES SAUVEGARDÉS EST OBLIGATOIRE À
        RESPECTER.
                    Des tests automatiques seront roulés lors de la correction
                    et ils prennent pour acquis que le format plus haut est
                    respecté. Vous perdrez des points si vous dérogez du format

        Args:
            nom_fichier: Le nom du fichier où sauvegarder, un string.
        """
        self.ma_partie = nom_fichier
        ma_partie = input("Nom du fichier : ")
        fichier = open("{}.txt", "x".format(ma_partie))
        fichier.write(self.couleur_joueur_courant + "\n" +
                      str(self.tour_precedent_passe) + "\n" +
                      str(self.deux_tours_passes) + "\n" +
                      str(self.joueur_blanc) + "\n" +
                      str(self.joueur_noir) + "\n" +
                      str(self.planche.convertir_en_chaine()))
        fichier.close()

    def charger(self, nom_fichier):
        """
        Charge une partie dans à partir d'un fichier. Le fichier a le même
        format que la méthode de sauvegarde.

        Args:
            nom_fichier: Le nom du fichier à charger, un string.
        """
        self.nom_fichier = nom_fichier
        nom_fichier = input("Entrez le nom de la partie à charger suivi de .txt : ")
        f = open(nom_fichier, "r")

        chaine = []

        while True:
            ligne = (f.readline().strip("\n"))
            if ligne:
                ligne = ligne.split(",")
                chaine.append(ligne)
            else:
                break


        self.planche.charger_dune_chaine(chaine)
        self.joueur_noir = chaine[3]
        self.joueur_blanc = chaine[4]
        self.joueur_courant = chaine[0]
        self.tour_precedent_passe = chaine[1]
        self.tour_precedent_passe = chaine[2]

        f.close()

