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
        self.__round = 1
        self.__current_player = 0

        self.__root=Tk()
        self.__root.resizable(False, False)
        self.__root.title("Jeu")
        
        self.__canvas=Canvas(self.__root, width=50*self.__board_length+50, height=50*self.__board_length+50)
        self.__canvas.bind("<Button-1>", self.handle_click)
        self.__canvas.pack()

        self.__pawns={}
        self.__colors={"pawns": ["red","blue"]}

        for i in range(self.__board_length+1):
            self.__canvas.create_line(25+i*50,25,25+i*50,25+50*self.__board_length)
            self.__canvas.create_line(25,25+i*50,25+50*self.__board_length,25+i*50)

        self.__player_var = StringVar()
        self.__player_var.set("Joueur 1")
        self.__player_text=Label(self.__root, textvariable=self.__player_var, font=('Helvetica', 20), pady=12)
        self.__player_text.pack()

    def switch_player(self):
        self.__current_player = (self.__current_player + 1) %2
        self.__player_var.set(f"Joueur {self.__current_player + 1}")

    def get_square(self,x,y):
        square_x = (x-25)//50
        square_y = (y-25)//50
        if square_x >= self.__board_length or square_y >= self.__board_length or square_x < 0 or square_y < 0:
            return None
        return {"x": square_x, "y": square_y}

    def handle_click(self,event):
        coordinates = self.get_square(event.x, event.y)
        if not coordinates:
            return
        
        if self.__round <= 2:
            # Placement des pions
            if self.__board[coordinates["y"]][coordinates["x"]] != None:
                return
            self.__board[coordinates["y"]][coordinates["x"]] = Pawn((coordinates["x"], coordinates["y"]), self.__current_player)
            shape=self.__canvas.create_oval(coordinates["x"]*50+30,coordinates["y"]*50+30,coordinates["x"]*50+70,coordinates["y"]*50+70, fill=self.__colors["pawns"][self.__current_player], width=0)
            self.__round += 1
            self.switch_player()
            
            

    def run(self):
        self.__root.mainloop()

game=Game()
game.run()
