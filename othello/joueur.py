from random import choice


class Joueur:
    """
    Classe générale de joueur. Vous est fournie.
    """

    def __init__(self, couleur):
        """
       Le constructeur global de Joueur.

       Args:
           couleur: La couleur qui sera jouée par le joueur.
       """

        assert couleur in ["blanc", "noir"], "Piece: couleur invalide."

        self.couleur = couleur

    def obtenir_type_joueur(self):
        """
        Cette méthode sera utilisée par les sous-classes JoueurHumain et
        JoueurOrdinateur.
        """

        pass

    def choisir_coup(self, coups_possibles):
        """
        Cette méthode sera implémentée par les sous-classes JoueurHumain et
        JoueurOrdinateur.
        """

        pass


class JoueurHumain(Joueur):
    """
    Classe modélisant un joueur humain.

        Args:
            Le joueur humain.
    """

    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la
        bonne couleur.

        Args:
            couleur: La couleur du joueur.
        """
        super().__init__(couleur)

    def obtenir_type_joueur(self):
        """
        Getter du type de joueur

        :returns: Le type de joueur, ici Humain
        """

        return "Humain"


class JoueurOrdinateur(Joueur):
    """
    Classe modélisant un joueur Ordinateur.

        Args:
            La couleur du joueur Ordinateur
    """

    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la
        bonne couleur.

        Args:
            La couleur du joueur

        """

        super().__init__(couleur)

    def obtenir_type_joueur(self):
        """
        Getter du type de joueur
        :returns: Le type de joueur, ici Ordinateur
        """

        return "Ordinateur"

    def choisir_coup(self, coups_possibles):
        """
        Intelligence artificielle du joueur ordinateur.

        Args:
            coups_possibles: Le dictionnaire des coups possibles

        Returns:
            un couple (ligne, colonne) représentant la position du coup désiré.
        """

        if len(coups_possibles) == 0:
            return -1, -1
        else:
            return choice(coups_possibles)
