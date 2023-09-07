"""Point d'entrée du programme"""

from battle.game import game_loop
from battle.home import display_rules, display_menu, say_goodbye, say_press_enter
from battle.stats import Stats
from time import time


def main():
    print("Bienvenue dans ce programme de jeu de bataille!")
    while True:
        choice = display_menu()
        match choice:
            case '1':
                display_rules()
                say_press_enter()
            case '2':
                game_loop()
                say_press_enter()
            case '3':
                valid_answer = False
                error_message = "Choix incorrect. Saisir un nombre entier supérieur à 1."
                while not valid_answer:
                    try:
                        answer = int(input("Sur combien de parties doit porter l'analyse statistique ? "))
                    except ValueError:
                        print(error_message)
                        continue
                    if answer > 1:
                        valid_answer = True
                        start_time = time()
                        data = game_loop(chosen_nb_games=answer, multigames_show_results=True)
                        end_time = time()
                        total_time = round(end_time - start_time, 2)
                        print(f"(Durée de l'opération: {total_time} secondes.)")
                        stats = Stats(data)
                        stats.display_stats()
                        print()
                        input("Appuyez sur Entrée pour afficher des graphiques...")
                        stats.display_graphics()
                        say_press_enter()
                    elif answer == 1:
                        print("Pour une partie simple, sélectionnez le choix 2 du menu principal.")
                    else:
                        print(error_message)
            case '4':
                say_goodbye()
                quit()


if __name__ == "__main__":
    main()
