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
# Méthodes : run, get_square, handle_click
class Game():
    def __init__(self):
        self.__board_length = askinteger("Jeu","Quelle est la taille du plateau (entre 8 et 12) ?")
        self.__win_length = askinteger("Jeu","Nombre de marques à aligner pour gagner (entre 4 et 6) ?")
        self.__board = [[None for i in range(self.__board_length)] for j in range(self.__board_length)]
        self.__root=Tk()
        self.__root.resizable(False, False)
        self.__root.title("Jeu")
        
        self.__canvas=Canvas(self.__root, width=50*self.__board_length+50, height=50*self.__board_length+50)
        self.__canvas.bind("<Button-1>", self.handle_click)
        self.__canvas.pack()

        for i in range(self.__board_length+1):
            self.__canvas.create_line(25+i*50,25,25+i*50,25+50*self.__board_length)
            self.__canvas.create_line(25,25+i*50,25+50*self.__board_length,25+i*50)

        self.__player_var = StringVar()
        self.__player_var.set("Joueur 1")
        self.__player_text=Label(self.__root, textvariable=self.__player_var, font=('Helvetica', 20), pady=12)
        self.__player_text.pack()

    def get_square(self,x,y):
        pass

    def handle_click(self,event):
        pass

    def run(self):
        self.__root.mainloop()

game=Game()
game.run()
