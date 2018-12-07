"""4.2  Créer la classe d’exception
ErreurPositionCoup
Nous vous demandons d’utiliser la gestion des exceptions pour gérer l’invalidité de la po-
sition d’un coup. Vous devez donc créer une nouvelle classe d’exception dans un fichier
exceptions.py
, puis modifier votre gestion des coups pour qu’un exception
ErreurPositionCoup
soit levée lorsque le coup tenté est invalide. Vous pourrez ajouter un message personnalisé à
l’exception lors de sa création pour vous permettre de savoir si l’invalidité du coup est dûe
à la présence d’une autre pièce ou encore à l’absence de pièces ”mangées”.
3
IFT-1004 — Introduction à la programmation
TP # 4
De cette manière, le code de votre interface n’aura pas à valider la position du coup soumise
par l’usager (avec un clic de souris) : si le coup demandé était invalide, aucun coup ne sera
joué et l’interface attrapera l’exception et affichera un message d’avertissement correspon-
dant."""


class ErreurPositionCoup(object):
    """
    Classe définissant les coups invalides et qui comporte des méthodes afin
    d'afficher à l'utilisateur un message correspondant. Le GUI pourra ainsi
    faire appel à ces listes pour valider le coup choisi par l'utilisateur
    sans faire appel au code central du jeu.
    """
    def __init__(self, listes_coups):
        self.coups_possibles = listes_coups[0]
        self.impossible_piece_la = listes_coups[1]
        self.impossible_zero_mangee = listes_coups[2]

    def verifier_coup_valide(self, coup_demander):
        """
        Prend en paramètre le coup demandé par l'utilisateur sur l'interface
        graphique et verifie s'il appartient à l'une des listes de coups
        possibles ou impossibles. Retourne si oui ou non le coup est possible
        et un message disant pourquoi il n'est pas possible. Si le coup
        n'appartient à aucune des listes, on indique qu'il est impossible car
        il ne respecte pas les bornes de la planche.

        :param coup_demander: Un tuple vectoriel de la position demandée par le
            joueur

        :return: Un tuple contenant un booléen disant si le coup est possible
            ou non, et un message à afficher à l'utilisateur si le coup n'est
            pas possible
        """

        if coup_demander in self.coups_possibles:
            return True, "ok"
        elif coup_demander in self.impossible_piece_la:
            return False, "Impossible, vous ne pouvez pas mettre une pièce " \
                          "par dessus une autre! "
        elif coup_demander in self.impossible_zero_mangee:
            return False, "Coup invalide. Aucune pièce ennemie ne serait " \
                          "mangée! "
        else:
            return False, "Une erreur s'est produite. La case sur laquelle " \
                          "vous voulez jouer n'existe pas sur la planche de " \
                          "jeu! "
