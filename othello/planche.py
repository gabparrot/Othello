from othello.piece import Piece


class Planche:
    """
    Classe représentant la planche d'un jeu d'Othello.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle planche.
        """
        # Dictionnaire de cases. La clé est une position (ligne, colonne), et la valeur une instance de la classe Piece.
        self.cases = {}

        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()

        # On joue au Othello 8x8
        self.nb_cases = 8

    def get_piece(self, position):
        """
        Récupère une pièce dans la planche.

        Args:
            position: La position où récupérer la pièce, un tuple de coordonnées matricielles (ligne, colonne).

        Returns:
            La pièce à cette position s'il y en a une, None autrement.
        """
        if position in self.cases:
            return self.cases[position]
        else:
            return None

        # TODO: Finie (J'pense)

    def position_valide(self, position):
        """
        Vérifie si une position est valide (chaque coordonnée doit être dans
        les bornes).

        Args:
            position: Un couple (ligne, colonne), tuple de deux éléments.

        Returns:
            True si la position est valide, False autrement
        """
        if position[0] in range(8) and position[1] in range(8):
            return True
        return False
        # TODO: Finie

    def obtenir_positions_mangees(self, position, couleur):
        """
        Détermine quelles positions seront mangées si un coup de la couleur passée est joué à la position passée.

        ***RETOURNEZ SEULEMENT LA LISTE DES POSITIONS MANGÉES, NE FAITES PAS APPEL À piece.echange_couleur() ICI.***

        Ici, commencez par considérer que, pour la position évaluée, des pièces peuvent être mangées dans 8 directions
        distinctes représentant les 8 cases qui entourent la position évaluée. Vous devez donc vérifier, pour chacune
        de ces directions, combien de pièces sont mangées et retourner une liste regroupant les pièces mangées dans
        toutes les directions.

        Ici, une direction représente une liste de 2 entiers pour la déplacement en x et y. Par exemple, pour la
        direction diagonale où en explore vers le bas et vers la droite, on utiliserait la liste [1, 1]. De même, pour
        la direction gauche, on utiliserait la liste [-1, 0]. Il y a donc un total de 8 directions, représentant les
        8 positions auxquelles la position actuelle peut toucher.

        Pensez à faire appel à la fonction obtenir_positions_mangees_direction().

        Args:
            position: La position du coup à jouer.
            couleur: La couleur du coup à jouer.

        Returns:
            une liste contenant toutes les positions qui seraient mangées par le coup.
        """
        # TODO: faire obtenir_positions_mangees_direction avant
        # TODO: appeller obtenir_posi... pour chaque direction. Ajouter chaque
        # TODO: return à une liste et retourner la liste finale
        # TODO: après appel pour Nord, Sud, Est, Ouest, Nord-Est, Nord-Ouest,
        # TODO: Sud-Est, Sud-Ouest
        # TODO: pour appel de obtenir_posi: position = coup joué, couleur du
        # TODO: joueur, direction cardinale
        pass

    def obtenir_positions_mangees_direction(self, couleur, direction, position):
        """
        Détermine les positions qui seront mangées si un coup de couleur "couleur" est joué à la position "position",
        si on parcourt la planche dans une direction "direction".

        Pour une direction donnée, vous devez parcourir la planche de jeu dans la direction. Tant que votre déplacement
        vous mène sur une pièce de la couleur mangée, vous continuez de vous déplacer. Trois situations surviennent
        alors pour mettre un terme au parours dans la direction :

        1) Vous arrivez sur une case vide. Dans ce cas, aucune pièce n'est mangée.

        2) Vous arrivez sur une case extérieure à la planche. Encore une fois, aucune pièce n'est mangée.

        3) Vous arrivez sur une case de la même couleur que le coup initial. Toutes les pièces de la couleur opposée
        que vous avez alors rencontrées dans votre parcours doivent alors être ajoutées à grande liste des pièces
        mangées cumulées.

        N.B. : Cette méthode peut être implémentée par au moins deux techniques différentes alors laissez place à votre
        imagination et explorez ! Une méthode faisant une boucle d'exploration complète et une méthode de parcours
        récursif  sont quelques-unes des façons de faire que vous pouvez explorer. Il se peut même que votre solution
        ne soit pas dans les solutions énumérées précédemment.

        Args:
            couleur: La couleur du coup évalué
            direction: La direction de parcours évaluée
            position: La position du coup évalué

        Returns:
            La liste (peut-être vide) de toutes les positions mangées à partir du coup et de la direction donnés.
        """
        # compliqué en esti ça caliss
        # TODO: possiblement dans un while loop qui break quand x or y == 8. Il
        # TODO: faut "parcourir la direction demandée à partir de position.
        # TODO: (Nord, Sud, Est, Ouest, NO, NE, SO, SE) avec un loop qui fait,
        # TODO: sur le vecteur position (x, y), une opération: {N(x, y+=1),
        # TODO: S(x,y-=1), E(x+=1,y), O(x-=1,y), NE(x+=1,y+=1) NO(x-=1,y+=1)
        # TODO: SE(x+=1,y-=1), SO(x-=1,y-=1)} À chaque opération, vérifier dans
        # TODO: if: if case vide: return None; if case couleur ennemi: append
        # TODO: liste de miam miam, si couleur joueur, return liste miam miam

        pass

    def coup_est_possible(self, position, couleur):
        """
        Détermine si un coup est possible. Un coup est possible si au moins une pièce est mangée par celui-ci.

        Args:
            position: La position du coup évalué
            couleur: La couleur du coup évalué

        Returns:
            True, si le coup est valide, False sinon
        """
        # TODO: if obtenir_positions_mangees() retourne une liste vide, return
        # TODO: False, else return True
        # TODO: si ya rien à bouffer dans la liste coup pas possible
        pass

    def lister_coups_possibles_de_couleur(self, couleur):
        """
        Fonction retournant la liste des coups possibles d'une certaine couleur. Un coup est considéré possible
        si au moins une pièce est mangée quand la couleur "couleur" joue à une certaine position, ne l'oubliez pas!

        ATTENTION: ne dupliquez pas de code déjà écrit! Réutilisez les fonctions déjà programmées!

        Args:
            couleur: La couleur ("blanc", "noir") des pièces dont on considère le déplacement, un string

        Returns:
            Une liste de positions de coups possibles pour la couleur "couleur"
        """
        # TODO: pour la couleur en arg, appeler "coup est possible" sur chaque
        # TODO: ostie de case du board, et append liste_coups_possibles avec la
        # TODO: position vérifiée chaque fois qu'on reçoit True.

        pass

    def jouer_coup(self, position, couleur):
        """
        Joue une pièce de la couleur "couleur" à la position "position".

        Cette méthode doit également:
        - Ajouter la pièce aux pièces de la planche.
        - Faire les changements de couleur pour les pièces mangées par le coup.
        - Retourner un message indiquant "ok" ou "erreur".

        ATTENTION: Ne dupliquez pas de code! Vous savez déjà qu'un coup est valide si au moins une pièce est mangée
                   par celui-ci. Vous avez une méthode qui fait exactement ce travail à programmer !

        Args:
            position: La position du coup.
            couleur: La couleur du coup.

        Returns:
            "ok" si le déplacement a été effectué car il est valide, "erreur" autrement.
        """
        # TODO: prendre un grand caliss de respire
        pass

    def convertir_en_chaine(self):
        """
        Retourne une chaîne de caractères où chaque case est écrite sur une ligne distincte.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder une planche dans un fichier.

        Returns:
            La chaîne de caractères.
        """
        # TODO: déboucher une bière pour oublier
        pass

    def charger_dune_chaine(self, chaine):
        """
        Remplit la planche à partir d'une chaîne de caractères comportant l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Args:
            chaine: La chaîne de caractères, un string.
        """
        # TODO: hurler
        pass

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
        Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Planche pour l'affichage.
        Faire un print(une_planche) affichera la planche à l'écran.
        """
        s = "  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, self.nb_cases):
            s += str(i)+" | "
            for j in range(0, self.nb_cases):
                if (i, j) in self.cases:
                    s += str(self.cases[(i, j)])+" | "
                else:
                    s += "  | "
            s += str(i)
            if i != self.nb_cases - 1:
                s += "\n  +---+---+---+---+---+---+---+---+\n"

        s += "\n  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"

        return s
