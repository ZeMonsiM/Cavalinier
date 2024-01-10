from tkinter import *

# Classe Pawn
# Représente le pion d'un joueur sur le plateau.
# Attributs : coordonnées (stockées dans un tuple (x,y)), joueur
# Méthodes : get_coordinates, get_player, can_move_to, is_stuck, move
Class Pawn():
    def __init__(self, coordinates: tuple, player):
        self.__coordinates = list(coordinates)
        self.__player = player

    def get_coordinates(self):
        return tuple(self.__coordinates)

    def get_player(self):
        return self.__player

    def can_move_to(self, coordinates: tuple, board):
        pass

    def is_stuck(self, board):
        pass

    def move(self, coordinates: tuple):
        pass

# Classe Game
# Gère toute la logique du jeu.
# TODO: Déterminer les attributs et les méthodes à mettre dans la classe
# Attributs : columns, rows
# Méthodes :
Class Game():
    def __init__(self):
        pass
