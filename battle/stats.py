"""Contient la classe Stats, pour générer des statistiques
sur une série de parties de bataille.
"""

from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np


class Stats:
    """Statistiques liées à une série de parties du jeu de bataille"""

    def __init__(self, data: Tuple[int, int, List[int], List[int]]):
        """Initialisation à partir du tuple des données de la série de parties.
        Ce tuple contient:
        - à l'indice 0, le nombre de victoires d'Alice
        - à l'indice 1, le nombre de victoires de Bob
        - à l'indice 2, la liste contenant le nombre de coups de chaque partie
        - à l'indice 3, la liste contenant le nombre de batailles de chaque partie.
        """

        # Propriétés liées au nombre de parties et de victoires
        self.player1_wins = data[0]
        self.player2_wins = data[1]
        self.nb_games = self.player1_wins + self.player2_wins
        self.player1_wins_percentage = round(self.player1_wins / self.nb_games * 100, 2)
        self.player2_wins_percentage = round(self.player2_wins / self.nb_games * 100, 2)

        # Propriétés liées au nombre de coups par partie
        self.nb_shots_data = data[2]
        self.total_shots = sum(self.nb_shots_data)
        self.shortest_game_nb_shots = min(self.nb_shots_data)
        self.longest_game_nb_shots = max(self.nb_shots_data)
        self.nb_shots_average = round(self.total_shots / self.nb_games)
        self.nb_shots_median = round(np.median(self.nb_shots_data))

        # Propriétés liées au nombre de batailles par partie
        self.nb_battles_data = data[3]
        self.battles_percentage_data = [round(self.nb_battles_data[i] * 100 / self.nb_shots_data[i], 2)
                                        for i in range(self.nb_games)]
        self.total_battles = sum(self.nb_battles_data)
        self.lowest_battles_percentage = min(self.battles_percentage_data)
        self.highest_battles_percentage = max(self.battles_percentage_data)
        self.nb_battles_average = round(self.total_battles / self.nb_games)
        self.nb_battles_median = round(np.median(self.nb_battles_data))
        self.battles_percentage_average = round(self.nb_battles_average * 100
                                                / self.nb_shots_average, 2)
        self.battles_percentage_median = np.median(self.battles_percentage_data)

    def __repr__(self):
        return f"Statistiques réalisées sur {self.nb_games} parties."

    def display_stats(self):
        """Affiche des statistiques sous forme de texte"""
        print()
        print("************")
        print("STATISTIQUES")
        print()
        print(f"Après {self.nb_games} parties terminées, ", end='')
        print(f"Alice gagne {self.player1_wins_percentage} % des parties,"
              f" et Bob {self.player2_wins_percentage} %.")
        print()
        print("Statistiques liées au NOMBRE DE COUPS:")
        print(f"- Le nombre médian de coups par partie est de {self.nb_shots_median}"
              f" coups.")
        print(f"- Le nombre moyen de coups par partie est de {self.nb_shots_average}"
              f" coups.")
        print(f"- La partie la plus courte a duré"
              f" {self.shortest_game_nb_shots} coups.")
        print(f"- La partie la plus longue a duré"
              f" {self.longest_game_nb_shots} coups.")
        print()
        print("Statistiques liées au NOMBRE DE BATAILLES:")
        print(f"- Le nombre médian de batailles par partie est de "
              f"{self.nb_battles_median} batailles.")
        print(f"- Le pourcentage médian de batailles par partie est de "
              f"{self.battles_percentage_median} % des coups joués.")
        print(f"- Le nombre moyen de batailles par partie est de "
              f"{self.nb_battles_average} batailles (soit "
              f"{self.battles_percentage_average} % des coups joués).")
        print(f"- Plus petit pourcentage de batailles dans une partie: {self.lowest_battles_percentage} %.")
        print(f"- Plus grand pourcentage de batailles dans une partie: {self.highest_battles_percentage} %.")

    def nb_shots_graph(self):
        """Génère un histogramme représentant la distribution du nombre de coups."""
        plt.hist(self.nb_shots_data, bins=30)
        plt.xlabel("Nombre de coups")
        plt.ylabel("Nombre de parties")
        plt.title("Distribution du nombre de coups joués par partie")
        plt.grid(True)

    def nb_battles_graph(self):
        """Génère un histogramme représentant la distribution du nombre de batailles."""
        plt.hist(self.nb_battles_data, bins=30)
        plt.xlabel("Nombre de batailles")
        plt.ylabel("Nombre de parties")
        plt.title("Distribution du nombre de batailles par partie")
        plt.grid(True)

    def display_graphics(self):
        """Affiche des statistiques sur le nombre de coups et de batailles
        sous forme de 2 graphiques côte à côte
        """
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        self.nb_shots_graph()
        plt.subplot(1, 2, 2)
        self.nb_battles_graph()
        plt.tight_layout()
        plt.show()
