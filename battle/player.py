"""Contient la classe Player, qui définit les joueurs·joueuses"""


from .collection import Collection


class Player:
    """Un·e joueur·joueuse"""

    def __init__(self, name):
        self.name = name
        self.hand = Collection()
        self.wins = 0

    def __repr__(self):
        return f"{self.name}"

    def take_discard_pile_cards(self, discard_pile: Collection):
        """Récupère en vrac toutes les cartes de la défausse"""
        discard_pile.shuffle_cards()  # nécessaire pour que la partie se termine à coup sûr
        for card in discard_pile.cards[::-1]:
            discard_pile.remove_card(card)
            self.hand.add_card(card)
            card.owned_by = self

    def reset(self):
        """Remet à 0 le nombre de cartes du joueur / de la joueuse.
        (Cette fonction nécessaire pour permettre l'enchaînement des parties.)
        """
        self.hand.cards = []
        self.hand.nb_cards = 0
