"""Contient des fonctions liées à l'écran d'accueil"""


def display_menu() -> str:
    """Affiche le menu d'accueil.
    Renvoie le choix valide de l'utilisateur·ice.
    """
    valid_choice = False
    while not valid_choice:
        print()
        print("Que voulez-vous faire ?")
        print("1 - Lire les règles du jeu de bataille")
        print("2 - Voir une partie aléatoire entre Alice et Bob")
        print("3 - Générer des statistiques")
        print("4 - Quitter le programme")
        print()
        choice = input("Votre choix ? ")
        if choice in ('1', '2', '3', '4'):
            return choice
        else:
            print()
            print("Choix invalide, saisissez juste le numéro de votre choix (1 à 4).")


def display_rules():
    """Ouvre le fichier game_rules.txt et affiche les règles du jeu de bataille"""
    with open("battle/game_rules.txt", "r") as f:
        print(f.read())


def say_press_enter():
    """Attend que l'utilisateur·ice appuie sur la touche Entrée"""
    input("(Appuyez sur Entrée pour revenir au menu...)")


def say_goodbye():
    """Message à afficher avant de quitter le programme"""
    print()
    print("Vous quittez le programme.")
    print("À bientôt !")
