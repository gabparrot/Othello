class ErreurPositionCoup(Exception):
    """
    Classe d'exceptions représentant un choix invalide de coup par
    l'utilisateur. Le GUI pourra ainsi faire appel à ces listes pour valider le coup choisi par l'utilisateur
    sans faire appel au code central du jeu.
    """
    pass
