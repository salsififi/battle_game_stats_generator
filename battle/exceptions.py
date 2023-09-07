"""Définit les exceptions potentielles"""


class MyAppException(Exception):
    """Classe de base pour les exceptions du programme"""
    pass


class GiveCardException(MyAppException):
    """Exception levée quand aucun·e joueur ou joueuse
    ne peut donner de carte à l'autre
    """

    def __init__(self):
        message = ("Cas rarissime d'une bataille où un·e joueur·joueuse n'a plus de "
                   "cartes, mais l'autre non plus!"
                   "Cela peut survenir suite à une avalanche de batailles depuis "
                   "le début de la partie, "
                   "dans le cas théorique où les joueuses et joueurs se voient "
                   "distribuer chacun des cartes de même valeur dans le même ordre, "
                   "malgré le mélange des cartes avant distribution.")
        super().__init__(message)


class InfiniteGameException(MyAppException):
    """Exception levée lorsqu'une partie dépasse les 10000 manches
    (dans le cas théorique où une configuration se répéterait indéfiniment,
    malgré le ramassage "en vrac" des cartes à chaque manche.
    """

    def __init__(self):
        message = ("Cas rare: partie extrêmement longue, probablement du fait "
                   "d'une configuration répétée indéfiniment.")
        super().__init__(message)
