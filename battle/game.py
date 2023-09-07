"""Contient la classe Game pour définir une partie.
Le coeur de ce module (et du projet) est la fonction game_loop.
"""


from sys import stdout
from .player import Player
from .collection import Collection, FullDeckCollection
from .card import Card
from .exceptions import GiveCardException, InfiniteGameException


class Game:
    """Une partie de bataille"""

    def __init__(self, player1: Player, player2: Player):
        self.players = (player1, player2)
        self.player1 = player1
        self.player2 = player2
        self.leading_player = player1
        self.low_ranking_player = player2
        self.deck = FullDeckCollection()
        self.discard_pile = Collection()
        self.nb_shots: int = 0  # nombre de manches (c'est-à-dire de coups hors bataille)
        self.nb_battles: int = 0  # nombre de batailles

    def __repr__(self):
        return f"Partie de bataille opposant{self.players[0]} à {self.players[1]}"

    def distribute_cards(self):
        """Distribue les cartes"""
        id_player = 0
        for card in self.deck.cards[::-1]:
            self.deck.remove_card(card)
            self.players[id_player].hand.add_card(card)
            card.owned_by = self.players[id_player]
            id_player += 1
            if id_player > 1:
                id_player = 0

    def play_cards(self, on_battle=False, hidden=False, nb_games=1):
        """Place la carte du haut de la pile de chaque joueur·joueuse dans la défausse
        Le paramètre 'on_battle' indique si les cartes sont jouées dans le cadre d'une bataille.
        Le paramètre 'hidden' indique si les cartes sont jouées faces cachées.
        Le paramètre 'nb_games' permet de différencier l'affichage en cas de partie unique.
        """
        if self.nb_shots >= 20000:
            raise InfiniteGameException()
        single_game = (nb_games == 1)
        if not on_battle:
            self.nb_shots += 1
            if single_game:
                print(f"Manche n°{self.nb_shots}:", end=" ")
        for player in self.players:
            first_card = player.hand.cards[0]
            if single_game:
                if not on_battle or not hidden:
                    print(f"{player} joue {first_card}.", end=" ")
                else:
                    print(f"{player} joue {first_card} face cachée.", end=" ")
            player.hand.remove_card(first_card)
            self.discard_pile.add_card(first_card)
        if single_game:
            print()

    def shot_winner(self):
        """Compare les 2 dernières cartes jouées.
        Renvoie l'objet Player correspondant à la plus forte carte jouée,
        ou renvoie None en cas d'égalité.
        """
        on_battle = False
        card1 = self.discard_pile.cards[-2]
        index1 = Card.all_values.index(card1.value)
        card2 = self.discard_pile.cards[-1]
        index2 = Card.all_values.index(card2.value)
        if index1 > index2:
            shot_winning_player = card1.owned_by
        elif index2 > index1:
            shot_winning_player = card2.owned_by
        else:
            on_battle = True
        if not on_battle:
            return shot_winning_player
        else:
            return None

    def give_card(self, nb_games=1):
        """Un·e joueur·joueuse donne une carte à l'autre.
        Nécessaire dans les cas où un·e joueur·joueuse n'a plus de cartes à poser
        lors d'une bataille.
        """
        if self.leading_player.hand.nb_cards < 2:
            raise GiveCardException()
        single_game = (nb_games == 1)
        card_to_give = self.leading_player.hand.cards[0]
        self.leading_player.hand.remove_card(card_to_give)
        self.low_ranking_player.hand.add_card(card_to_give)
        card_to_give.owned_by = self.low_ranking_player
        if single_game:
            print(f"{self.leading_player} donne une carte à {self.low_ranking_player}.")


def game_loop(chosen_nb_games: int = 1, multigames_show_results=False):
    """Boucle de jeu d'une partie aléatoire, qui sera répétée 'nb_games' fois.
    L'affichage de tout le détail étape par étape n'est réalisée que
    si chosen_nb_games vaut 1.
    Le paramètre 'multigames_shox_results' permet de diminuer un peu le
    temps de traitement, s'il a pour valeur False
    Renvoie un tuple contenant les données générées par les parties
    si chosen_nb_games > 1, ne renvoie rien sinon.
    Données renvoyées dans le tuple:
    - nombre de victoire d'Alice
    - nombre de victoires de Bob
    - liste contenant le nombre de coups de chaque partie
    - liste contenant le nombre de batailles de chaque partie.
    """

    player1 = Player("Alice")
    player2 = Player("Bob")
    nb_shots_data = []
    nb_battles_data = []
    single_game = (chosen_nb_games == 1)

    for id_game in range(1, chosen_nb_games+1):

        # Création de la partie
        battle_game = Game(player1, player2)
        battle_game.distribute_cards()
        end_game = False
        infinite_game = False  # pour gérer le cas théorique de partie sans fin possible
        battles_avalanche = False  # pour gérer le cas du match nul par défaut de cartes
        battle = False

        # Boucle de jeu
        while not end_game and not infinite_game and not battles_avalanche:

            # Chaque joueur·joueuse pose une carte
            if not battle:
                try:
                    battle_game.play_cards(nb_games=chosen_nb_games)
                except InfiniteGameException:
                    infinite_game = True
                    break
            else:
                battle_game.play_cards(on_battle=True, nb_games=chosen_nb_games)
                battle = False

            # On détermine qui gagne, ou s'il y a "bataille"
            shot_winner = battle_game.shot_winner()
            if shot_winner:
                shot_winner.take_discard_pile_cards(battle_game.discard_pile)
                if battle_game.player1.hand.nb_cards > battle_game.player2.hand.nb_cards:
                    battle_game.leading_player = battle_game.player1
                    battle_game.low_ranking_player = battle_game.player2
                else:
                    battle_game.leading_player = battle_game.player2
                    battle_game.low_ranking_player = battle_game.player1
                if single_game:
                    print(f"{shot_winner} prend les cartes.", end=" ")
                    print(f"{battle_game.player1} a maintenant {battle_game.player1.hand.nb_cards} cartes,"
                          f" et {battle_game.player2} {battle_game.player2.hand.nb_cards}.")
            else:
                if single_game:
                    print("BATAILLE !!!")
                battle = True
                battle_game.nb_battles += 1
                # Gestion du cas où un·e joueur·joueuese n'a plus de cartes
                if battle_game.low_ranking_player.hand.nb_cards == 0:
                    try:
                        battle_game.give_card(nb_games=chosen_nb_games)
                    except GiveCardException:
                        print("Les joueurs·joueuses n'ont plus assez de cartes pour continuer.")
                        print("Pas de vainqueur, fin de la partie.")
                        battles_avalanche = True
                        break
                # Cas général:
                try:
                    battle_game.play_cards(on_battle=True, hidden=True, nb_games=chosen_nb_games)
                except InfiniteGameException:
                    infinite_game = True
                    break
                if battle_game.low_ranking_player.hand.nb_cards == 0:
                    battle_game.give_card(nb_games=chosen_nb_games)
            end_game = (player1.hand.nb_cards == 54) or (player2.hand.nb_cards == 54)

        # Annonce du résultat
        if battles_avalanche:
            print(f"Partie n°{id_game}: avalanche de batailles, plus assez de cartes!")
            print("Pas de vainqueur, la partie s'arrête.")
        elif infinite_game:
            print(f"Partie n°{id_game}: la partie est exceptionnellement longue. "
                  f"Vous êtes peut-être dans une configuration où le jeu ne peut "
                  f"jamais se terminer.")
            print("Pas de vainqueur, la partie s'arrête.")
        else:
            if single_game:
                print()
                print("PARTIE FINIE!")
                print(f"{shot_winner} gagne, après {battle_game.nb_shots} manches et "
                      f"{battle_game.nb_battles} batailles.")
            if not single_game and multigames_show_results:
                stdout.write(f"Partie n°{id_game}: {shot_winner} gagne, après {battle_game.nb_shots} manches "
                             f"et {battle_game.nb_battles} batailles.\n")

        # réinitialisation des jeux des joueurs·joueuses (nécessaire pour enchaîner les parties)
        for player in battle_game.players:
            player.reset()

        # sauvegarde des données avant la partie suivante
        if not single_game and not infinite_game and not battles_avalanche:
            shot_winner.wins += 1
            nb_shots_data.append(battle_game.nb_shots)
            nb_battles_data.append(battle_game.nb_battles)

    if not single_game:
        return player1.wins, player2.wins, nb_shots_data, nb_battles_data
