"""Définit les différentes classes de cartes à jouer"""


from abc import ABC


class Card(ABC):
    """Classe de base abstraite pour définir une carte à jouer"""

    all_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi', 'as', 'joker']

    def __init__(self, value, owned_by=None):
        self.value = value
        self.owned_by = owned_by


class JokerCard(Card):
    """Un joker"""

    def __init__(self):
        super().__init__(self.all_values[-1])

    def __str__(self):
        return "Joker"

    def __repr__(self):
        return str(self)


class ColoredCard(Card):
    """Une carte de l'une des quatre familles traditionnelles: coeur, carreau, pique, trèfle"""

    families = ['coeur', 'carreau', 'pique', 'trèfle']
    values = Card.all_values[:-1]

    def __init__(self, value, family):
        super().__init__(value)
        self.family = family

    def __repr__(self):
        return f"{self.value} de {self.family}"
