"""
Module principal du package othello. C'est ce module que nous allons exécuter
pour démarrer votre jeu.
"""

from interface.interface_othello import Application

if __name__ == '__main__':
    # Création d'une instance de Partie.
    jeu = Application()
    jeu.mainloop()

    # # Si on veut charger une partie à partir d'une partie sauvegardée.
    # partie = Partie("partie_un_tour_a_passer.txt")

    # # Si on veut sauvegarder une partie.
    # partie.sauvegarder("ma_partie.txt")

    # Démarrage de cette partie.
    # partie.jouer()
