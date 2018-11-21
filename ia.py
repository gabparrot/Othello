class IntelligenceArtificielle(Planche):
    """
    Classe représentant l'intelligence artificielle de l'ordinateur et
    possédant des méthodes de tris pour déterminer les meilleurs coups
    possibles
    """
    def __init__(self):
        super().__init__()
        self.coups_les_plus_forts = []

    def filtrer_meilleurs_coups(self, coups_possibles, couleur):
        """
        Prend la liste des coups possibles et retourne une liste contenant le
        ou les meilleurs coups dans une liste de tuple positionnels selon la
        stratégie de contrôle des coins suivante, dans cet ordre de priorités:

        1- Les coins;
        2- Les cases à 2 cases des coins, en lignes droite;
        3- Les cases à 2 cases des coins, en diagonale;
        Si plusieurs coups aussi forts ou si aucun ne correspond à 1, 2 et 3
           appelle IA_empecher_coins_ennemi() pour tenter
           d'empecher l'adversaire de jouer les cas 1-, 2- ou 3- au prochain
           tour
        Parmis les coups restant, priorise dans cet ordre:
        4- Les cases qui bordent les côtés de la planche;
        5- Les coups qui mangent le plus de pièces;
        6- Si plusieurs coups aussi forts restent, appelle IA_nuire_ennemi
           pour garder les coups qui limiteront le plus possible le nombre de
           pièces mangées par l'adversaire au prochain tour

        Nous retournons une liste contenant le meilleur coup s'il n'y en a
        qu'un, ou la liste de tous les meilleurs coups égaux

        :param coups_possibles: liste des coups possibles pour le joueur
                                ordinateur courant.

        :return: liste de tuples représentant le ou les meilleurs coups à jouer
        """
        coins = [(0, 0), (0, self.nb_cases), (self.nb_cases, 0),
                 (self.nb_cases, self.nb_cases)]

        deux_cases_du_coin_en_ligne = [(0, 2), (2, 0), (0, self.nb_cases -2),
                                       (2, self.nb_cases),(self.nb_cases -2, 0)
                                       , (self.nb_cases, 2),
                                       (self.nb_cases -2, self.nb_cases),
                                       (self.nb_cases, self.nb_cases -2)]

        deux_cases_du_coin_en_diago = [(2, 2), (2, self.nb_cases -2),
                                       (self.nb_cases -2, 2),
                                       (self.nb_cases -2, self.nb_cases -2)]
        cases_bordures = []
        for i in range (self.nb_cases):
            for j in range (self.nb_cases):
                if j in [0, self.nb_cases]:
                    cases_bordures.append((i,j))
                elif i in (0, self.nb_cases):
                    cases_bordures.append((i,j))
        self.coups_les_plus_forts.clear()

        # Si aucun coup possible retourner un coup qu'on sait invalide
        if len(coups_possibles) < 1:
            return -1, -1

        # si on peut jouer des coins, en faire la liste
        for coup in coups_possibles:
            if coup in coins:
                coups_les_plus_forts.append(coup)

        # Si 1 coin jouable, le retourne, si plus qu'un, fait tri_vs_ennemi()
        if len(coups_les_plus_forts) == 1:
            return coups_les_plus_forts
        elif self.tri_vs_ennemi(coups_les_plus_forts, couleur):
            return self.tri_vs_ennemi(coups_les_plus_forts, couleur)

        # Si aucun coin jouable, recommence avec priorité 2
        for coup in coups_possibles:
            if coup in deux_cases_du_coin_en_ligne:
                coups_les_plus_forts.append(coup)

        if len(coups_les_plus_forts) == 1:
            return coups_les_plus_forts
        elif self.tri_vs_ennemi(coups_les_plus_forts, couleur):
            return self.tri_vs_ennemi(coups_les_plus_forts, couleur)

        # Si aucun jouable en priorité 2, recommene avec priorité 3

        for coup in coups_possibles:
            if coup in deux_cases_du_coin_en_diago:
                coups_les_plus_forts.append(coup)

        if len(coups_les_plus_forts) == 1:
            return coups_les_plus_forts
        elif self.tri_vs_ennemi(coups_les_plus_forts, couleur):
            return self.tri_vs_ennemi(coups_les_plus_forts, couleur)

        # Si aucun en priorité 3, on recommence avec priorité 4: bordures

        coups_les_plus_forts = self.tri_vs_ennemi(coups_possibles, couleur)
        if len(coups_les_plus_forts) == 1:
            return coups_les_plus_forts

        coups_de_bordures = []
        for coup in coups_les_plus_forts:
            if coup in cases_bordures:
                coups_de_bordures.append(coup)

        if len(coups_de_bordures) == 1:
            return coups_de_bordures
        elif self.tri_vs_ennemi(coups_de_bordures, couleur):
            return self.tri_vs_ennemi(coups_de_bordures, couleur)

        # Si aucun en priorité 4, on recommence avec priorité 5, le plus de
        # pions mangés possible. On compte avec obtenir_position_mangees()
        else:
            max_manger = 0
            for coup in coups_les_plus_forts:
                if self.obtenir_positions_mangees(coup, couleur):

    def coups_coins(self, coups_possibles, couleur):
        """
        Permet de vérifier si l'IA peut jouer des coups sur les coins de la
        planche. Si plusieurs coups aux coins sont possibles, elle tente de
        trouver le meilleur coup en appelant tri_vs_ennemi(), puis s'il en
        reste toujours plusieurs, en appelant limiter_degats(). Elle retourne
        le meilleur coup ou les meilleurs coups égaux dans une liste. S'il n'y
        en a aucun, elle retourne None

        :param coups_possibles: liste des coups possibles

        :param couleur: couleur du joueur courant

        :return: le ou les coups aux coins, None sinon
        """
        coins = [(0, 0), (0, self.nb_cases), (self.nb_cases, 0),
                 (self.nb_cases, self.nb_cases)]

        for coup in coups_possibles:
            if coup in coins:
                self.coups_les_plus_forts.append(coup)
        return self.tri_vs_ennemi(self.coups_les_plus_forts, couleur)


        if len(self.coups_les_plus_forts) == 1:
            return self.coups_les_plus_forts
        else:
            return self.limiter_degats(self.coups_les_plus_forts, couleur)

    def coups_2_cases_du_coin_en_ligne(self, coup_possibles, couleur):
        """

        :param coup_possibles:
        :param couleur:
        :return:
        """


    def tri_vs_ennemi(self, coups_les_plus_forts, couleur):
        if len(self.coups_les_plus_forts) == 0:
            return None
        elif len(self.coups_les_plus_forts) == 1:
            return self.coups_les_plus_forts
        else:
            if not self.ennemi_condition_1(self.coups_les_plus_forts, couleur):
                return self.coups_les_plus_forts
            else:
                if len(self.ennemi_condition_1(
                        self.coups_les_plus_forts, couleur)) == 1:
                    return self.ennemi_condition_1(self.coups_les_plus_forts,
                                                   couleur)
                else:

                    if not self.ennemi_condition_2(self.coups_les_plus_forts,
                                                   couleur):
                        return self.coups_les_plus_forts



        # coups_restants = []
        # if len(coups_les_plus_forts) > 1:
        #     coups_restants = self.empecher_coins_ennemi(
        #                      coups_les_plus_forts)
        #     if len(coups_restants) > 1:
        #         return self.limiter_degats(coups_restants)
        #     else:
        #         return coups_restants
        # else:
        #     return False



    def ennemi_condition_1(self, coups_les_plus_forts, couleur):
        coups_trier = []
        return coups_trier

    def ennemi_condition_2(self, coups_les_plus_forts, couleur):
        coups_trier = []
        return coups_trier

    def limiter_degats(self, coups_restants, couleur):
        """
        Cette méthode est appelée par filtrer_meilleurs_coups() si celle-ci
        trouve plusieurs meilleurs coups égaux, afin de déterminer lequel de
        ces coups nuit le plus au joueur adverse
        :return:
        """
        return -1, -1