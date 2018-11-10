from othello.planche import Planche
from othello.joueur import JoueurOrdinateur, JoueurHumain
types_joueurs = ("Humain", "Ordinateur")

class Partie:
    def __init__(self, nom_fichier=None):
        """
        Méthode d'initialisation d'une partie. On initialise 4 membres:
        - planche: contient la planche de la partie, celui-ci contenant le dictionnaire de pièces.
        - couleur_joueur_courant: le joueur à qui c'est le tour de jouer.
        - tour_precedent_passe: un booléen représentant si le joueur précédent a passé son tour parce qu'il
           n'avait aucun coup disponible.
        - deux_tours_passes: un booléen représentant si deux tours ont été passés de suite, auquel cas la partie
           devra se terminer.
        - coups_possibles : une liste de tous les coups possibles en fonction de l'état actuel de la planche,
           initialement vide.

        On initialise ensuite les joueurs selon la paramètre nom_fichier. Si l'utilisateur a précisé un nom_fichier,
        on fait appel à la méthode self.charger() pour charger la partie à partir d'un fichier. Sinon, on fait appel
        à self.initialiser_joueurs(), qui va demander à l'utilisateur quels sont les types de joueurs qu'il désire.
        """
        self.planche = Planche()

        self.couleur_joueur_courant = "noir"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

    def initialiser_joueurs(self):
        """
        On initialise ici trois attributs : joueur_noir, joueur_noir et joueur_courant (initialisé à joueur_noir).

        Pour créer les objets joueur, faites appel à demander_type_joueur()
        """

        self.joueur_noir = self.demander_type_joueur("noir")
        self.joueur_blanc = self.demander_type_joueur("blanc")
        self.joueur_courant = ("noir") #pascorrectpasmalsûr
        #TODO initialiser jouer_courant correctement

    def demander_type_joueur(self, couleur):
        """
        Demande à l'usager quel type de joueur ('Humain' ou 'Ordinateur') il désire pour le joueur de la couleur.

        Tant que l'entrée n'est pas valide, on continue de demander à l'utilisateur.

        Faites appel à self.creer_joueur() pour créer le joueur lorsque vous aurez le type.

        Args:
            couleur: La couleur pour laquelle on veut le type de joueur.

        Returns:
            Un objet Joueur, de type JoueurHumain si l'usager a entré 'Humain', JoueurOrdinateur s'il a entré
            'Ordinateur'.
        """
        type_joueur = ""
        while type_joueur not in types_joueurs:
            type_joueur = (f"Est-ce que le joueur {couleur} sera un Humain ou"
                           " un Ordinateur? ").title()
            if type_joueur not in types_joueurs:
                print("Erreur, type invalide, veuillez réessayer.")
            else:
                return self.creer_joueur(type_joueur, couleur)


    def creer_joueur(self, type, couleur):
        """
        Crée l'objet Joueur approprié, selon le type passé en paramètre.

        Pour créer les objets, vous n'avez qu'à faire appel à leurs constructeurs, c'est-à-dire à
        JoueurHumain(couleur), par exemple.

        Args:
            type: le type de joueur, "Ordinateur" ou "Humain"
            couleur: la couleur du pion joué par le jouer, "blanc" ou "noir"

        Returns:
            Un objet JoueurHumain si le type est "Humain", JoueurOrdinateur sinon
        """
        if type == "Ordinateur":
            joueur = JoueurOrdinateur(couleur)
            return joueur
        else:
            joueur = JoueurHumain(couleur)
            return joueur

    def valider_position_coup(self, position_coup):
        """
        Vérifie la validité de la position désirée pour le coup. On retourne un message d'erreur approprié pour
        chacune des trois situations suivantes :

        1) Le coup tenté ne représente pas une position valide de la planche de jeu.

        2) Une pièce se trouve déjà à la position souhaitée.

        3) Le coup ne fait pas partie de la liste des coups valides.

        ATTENTION: Utilisez les méthodes et attributs de self.planche ainsi que la liste self.coups_possibles pour
                   connaître les informations nécessaires.
        ATTENTION: Bien que cette méthode valide plusieurs choses, les méthodes programmées dans la planche vous
                   simplifieront la tâche!

        Args:
            position_coup: La position du coup à valider.

        Returns:
            Un couple où le premier élément représente la validité de la position (True ou False), et le
            deuxième élément est un éventuel message d'erreur.
        """
        pass

    def tour(self):
        """
        Cette méthode simule le tour d'un joueur, et doit effectuer les actions suivantes:
        - Demander la position du coup au joueur courant. Tant que la position n'est pas validée, on continue de
          demander. Si la position est invalide, on affiche le message d'erreur correspondant. Pour demander la
          position, faites appel à la fonction choisir_coup de l'attribut self.joueur_courant, à laquelle vous
          devez passer la liste de coups possibles. Pour valider le coup retourné, pensez à la méthode de validation
          de coup que vous avez déjà à implémenter.
        - Jouer le coup sur la planche de jeu, avec la bonne couleur.
        - Si le résultat du coup est "erreur", afficher un message d'erreur.

        ***Vous disposez d'une méthode pour demander le coup à l'usager dans cette classe et la classe planche
        possède à son tour une méthode pour jouer un coup, utilisez-les !***
        """
        pass

    def passer_tour(self):
        """
        Affiche un message indiquant que le joueur de la couleur courante ne peut jouer avec l'état actuel de la
        planche et qu'il doit donc passer son tour.
        """
        print(f"Aucun coup possible, joueur {self.couleur_joueur_courant} passe son tour")

    def partie_terminee(self):
        """
        Détermine si la partie est terminée, Une partie est terminée si toutes les cases de la planche sont remplies
        ou si deux tours consécutifs ont été passés (pensez à l'attribut self.deux_tours_passes).
        """
        pass

    def determiner_gagnant(self):
        """
        Détermine le gagnant de la partie. Le gagnant est simplement la couleur pour laquelle il y a le plus de
        pions sur la planche de jeu.

        Affichez un message indiquant la couleur gagnante ainsi que le nombre de pièces de sa couleur ou encore
        un message annonçant un match nul, le cas échéant.
        """
        pass

    def jouer(self):
        """
        Démarre une partie. Tant que la partie n'est pas terminée, on fait les choses suivantes :

        1) On affiche la planche de jeu ainsi qu'un message indiquant à quelle couleur c'est le tour de jouer.
           Pour afficher une planche, faites appel à print(self.planche)

        2) On détermine les coups possibles pour le joueur actuel. Pensez à utiliser une fonction que vous avez à
           implémenter pour Planche, et à entreposer les coups possibles dans un attribut approprié de la partie.

        3) Faire appel à tour() ou à passer_tour(), en fonction du nombre de coups disponibles pour le joueur actuel.
           Mettez aussi à jour les attributs self.tour_precedent_passe et self.deux_tours_passes.

        4) Effectuer le changement de joueur. Modifiez à la fois les attributs self.joueur_courant et
           self.couleur_joueur_courant.

        5) Lorsque la partie est terminée, afficher un message mentionnant le résultat de la partie. Vous avez une
           fonction à implémenter que vous pourriez tout simplement appeler.
        """
        pass

    def sauvegarder(self, nom_fichier):
        """
        Sauvegarde une partie dans un fichier. Le fichier condiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le tour précédent a été passé.
        - Une ligne contenant True ou False, si les deux derniers tours ont été passés.
        - Une ligne contenant le type du joueur blanc.
        - Une ligne contenant le type du joueur noir.
        - Le reste des lignes correspondant à la planche. Voir la méthode convertir_en_chaine de la planche
         pour le format.

        ATTENTION : L'ORDRE DES PARAMÈTRES SAUVEGARDÉS EST OBLIGATOIRE À RESPECTER.
                    Des tests automatiques seront roulés lors de la correction et ils prennent pour acquis que le
                    format plus haut est respecté. Vous perdrez des points si vous dérogez du format.

        Args:
            nom_fichier: Le nom du fichier où sauvegarder, un string.
        """
        pass

    def charger(self, nom_fichier):
        """
        Charge une partie dans à partir d'un fichier. Le fichier a le même format que la méthode de sauvegarde.

        Args:
            nom_fichier: Le nom du fichier à charger, un string.
        """
        pass
