class ErreurPositionCoup(Exception):
    """
    Classe d'exceptions représentant un choix invalide de coup par
    l'utilisateur. Le GUI pourra ainsi faire appel à ces listes pour valider
    le coup choisi par l'utilisateur sans faire appel au code central du jeu.
    """

    pass


class ErreurChoix(Exception):
    """
    Classe d'erreur servant à attraper des données invalides lors des choix de
    l'utilisateur au début de la partie. Ou si celui-ci ferme les fenêtres
    TopLevel sans répondre
    """

    pass
