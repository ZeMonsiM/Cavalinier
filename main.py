from tkinter import *
from tkinter.simpledialog import askinteger

# Classe Pawn
# Représente le pion d'un joueur sur le plateau.
# Attributs : coordonnées (stockées dans un tuple (x,y)), joueur
# Méthodes : get_coordinates, get_player, can_move_to, is_stuck, move
class Pawn():
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
# Attributs : board_length, board, root, win_length
# Méthodes :
class Game():
    def __init__(self):
        self.__board_length = askinteger("Jeu","Quelle est la taille du plateau (entre 8 et 12) ?")
        self.__win_length = askinteger("Jeu","Nombre de marques à aligner pour gagner (entre 4 et 6) ?")
        self.__board = [[None for i in range(self.__board_length)] for j in range(self.__board_length)]
        print(self.__board)

Game()
