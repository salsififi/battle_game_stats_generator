"""Contient des classes définissant les différents types de
collections de cartes à jouer
"""


from random import shuffle
from typing import List
from .card import Card, JokerCard, ColoredCard


class Collection:
    """Une collection de cartes à jouer"""

    def __init__(self):
        """Collection vide à l'initialisation"""
        self.cards: List[Card] = []
        self.nb_cards = 0

    def __repr__(self):
        return f"Contient: {self.cards}"

    def add_card(self, card: Card):
        """Ajoute une carte dans la collection"""
        self.cards.append(card)
        self.nb_cards += 1

    def remove_card(self, card: Card):
        """Retire une carte de la collection"""
        self.cards.remove(card)
        self.nb_cards -= 1

    def shuffle_cards(self):
        """Mélange les cartes"""
        shuffle(self.cards)


class FullDeckCollection(Collection):
    """Jeu de cartes complet et mélangé"""

    def __init__(self):
        """Crée un jeu de 54 cartes (toutes les familles colorées + 2 jokers)"""
        super().__init__()
        for value in ColoredCard.values:
            for family in ColoredCard.families:
                card = ColoredCard(value, family)
                self.add_card(card)
        for i in range(2):
            self.add_card(JokerCard())
        self.shuffle_cards()

    def __repr__(self):
        return f"Jeu de 54 cartes"
