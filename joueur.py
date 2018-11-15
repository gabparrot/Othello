from random import choice
#TODO en théorie la partie joueur.py est finie (fonctionnelle, optimisable)

class Joueur:
    """
    Classe générale de joueur. Vous est fournie.
    """
    #TODO on touche aucune méthode de la classe Joueur, tout est tiguidou
    def __init__(self, couleur):
        """
        Le constructeur global de Joueur.

        Args:
            couleur: La couleur qui sera jouée par le joueur.
        """
        assert couleur in ["blanc", "noir"], "Piece: couleur invalide."

        self.couleur = couleur

    def obtenir_type_joueur(self):
        '''
        Cette méthode sera utilisée par les sous-classes JoueurHumain et JoueurOrdinateur.

        Returns:
            Le type de joueur, 'Ordinateur' ou 'Humain'
        '''
        pass

    def choisir_coup(self, coups_possibles, range_possible):
        '''
        Cette méthode sera implémentée par les sous-classes JoueurHumain et JoueurOrdinateur.

        Args:
            coups_possibles: la liste des coups possibles

        Returns:
            un couple (ligne, colonne) représentant la positon du coup désiré.
        '''
        pass


class JoueurHumain(Joueur):
    """
    Classe modélisant un joueur humain.
    """

    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la bonne couleur.
        """
        super().__init__(couleur)
        #TODO finie

    def obtenir_type_joueur(self):
        return "Humain"
        #TODO finie

    def choisir_coup(self, coups_possibles):
        """
        Demande successivement à l'usager à quelle ligne, puis à quelle
        colonne il désire jouer.

        Nous vous avons déjà fourni une portion de code permettant d'attrapper
        au passage les erreurs qui peuvent survenir lorsque l'utilisateur entre
        autre chose qu'un nombre entier.

        Args:
            coups_possibles: La liste des coups possibles

        Returns:
            un couple (ligne, colonne) représentant la position du coup désiré.
        """
        try:
            input_row = int(input("Sur quelle ligne (0 à 7) voulez vous jouer votre coup? "))
            input_col = int(input("Et sur quelle colonne? (0 à 7) "))
            if input_col in range(nb)
            return(input_row, input_col)

        except ValueError:
            print("Position invalide.\n")
            print("")
            # L'usager a fait une erreur de saisie, on retourne donc un coup que l'on sait invalide.
            # Ceci forcera le programme à redemander le coup au joueur.
            return (-1, -1)
        #TODO: Finie (supposé =/)


class JoueurOrdinateur(Joueur):
    """
    Classe modélisant un joueur Ordinateur.
    """
    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la
        bonne couleur.
        """
        super().__init__(couleur)
        #TODO finie

    def obtenir_type_joueur(self):
        return "Ordinateur"
        #TODO finie

    def choisir_coup(self, coups_possibles):
        """
        Pour votre joueur ordinateur, vous n'avez qu'à sélectionner un coup au
        hasard parmi la liste des coups possibles. Affichez ensuite en console
        les numéros de ligne et de colonne.

        Pour faire un choix au hasard, vous devrez faire appel à la libraire
        random de Python. Explorez là, elle possède même une fonction
        retournant précisément un choix aléatoire parmi une liste.

        Args:
            coups_possibles: La liste des coups possibles

        Returns:
            un couple (ligne, colonne) représentant la position du coup désiré.
        """
        return choice(coups_possibles)
        #TODO finie                 (fonctionnelle, peut être améliorée)
        #TODO possiblement retourner qu'on passe le tour si coups_possibles est vide
        #TODO possiblement faire meillleure AI pour choisir coup optimal par ordi
