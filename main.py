from tkinter import *
from tkinter.simpledialog import askinteger
from tkinter.messagebox import showerror, showinfo

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

    def can_move_to(self, destination: tuple, board, board_length):
        x,y = self.__coordinates[0], self.__coordinates[1]
        if x < board_length - 1 and y > 1 and board[y-2][x+1] == None and destination == (x+1,y-2):
            return True
        if x < board_length - 2 and y > 0 and board[y-1][x+2] == None and destination == (x+2,y-1):
            return True
        if x < board_length - 2 and y < board_length - 1 and board[y+1][x+2] == None and destination == (x+2,y+1):
            return True
        if x < board_length - 1 and y < board_length - 2 and board[y+2][x+1] == None and destination == (x+1,y+2):
            return True
        if x > 0 and y < board_length - 2 and board[y+2][x-1] == None and destination == (x-1,y+2):
            return True
        if x > 1 and y < board_length - 1 and board[y+1][x-2] == None and destination == (x-2,y+1):
            return True
        if x > 1 and y > 0 and board[y-1][x-2] == None and destination == (x-2,y-1):
            return True
        if x > 0 and y > 1 and board[y-2][x-1] == None and destination == (x-1,y-2):
            return True
        return False

    def is_stuck(self, board, board_length):
        pass

    def move(self, coordinates: tuple, board):
        old_coordinates = self.__coordinates
        self.__coordinates = [coordinates[0], coordinates[1]] # Changement des coordonnées
        board[old_coordinates[1]][old_coordinates[0]] = self.__player # Rajouter la marque du joueur
        board[self.__coordinates[1]][self.__coordinates[0]] = "." # Déplacer le pion dans le board
        # TODO: Code de l'interface utilisateur (déplacement du pion et création du marqueur)

# Classe Game
# Gère toute la logique du jeu.
# TODO: Déterminer les attributs et les méthodes à mettre dans la classe
# Attributs : board_length, board, root (+ autres éléments de l'interface graphique), win_length, pawns, colors, player_var
# Méthodes : run, get_square, handle_click, switch_player, parameters_are_valid
class Game():
    def __init__(self, use_default_values=False):
        if not use_default_values:
            self.__board_length = askinteger("Jeu","Quelle est la taille du plateau (entre 8 et 12) ?")
            self.__win_length = askinteger("Jeu","Nombre de marques à aligner pour gagner (entre 4 et 6) ?")

            if not self.parameters_are_valid(self.__board_length, self.__win_length):
                showerror("Erreur","Les paramètres de jeu sont incorrects ! Veuillez vérifier que la taille du plateau et que la condition de victoire soient bien configurées et réessayez.")
                exit()
        else:
            self.__board_length = 10
            self.__win_length = 5

        self.__board = [[None for i in range(self.__board_length)] for j in range(self.__board_length)]
        self.__pawns = [None, None]
        self.__shapes = [None, None]
        self.__round = 1
        self.__current_player = 0

        self.__root=Tk()
        self.__root.resizable(False, False)
        self.__root.title("Jeu")
        
        self.__canvas=Canvas(self.__root, width=50*self.__board_length+50, height=50*self.__board_length+50)
        self.__canvas.bind("<Button-1>", self.handle_click)
        self.__canvas.pack()

        self.__colors={"pawns": ["red","blue"]}

        for i in range(self.__board_length+1):
            self.__canvas.create_line(25+i*50,25,25+i*50,25+50*self.__board_length)
            self.__canvas.create_line(25,25+i*50,25+50*self.__board_length,25+i*50)

        self.__player_var = StringVar()
        self.__player_var.set("Joueur 1")
        self.__player_text=Label(self.__root, textvariable=self.__player_var, font=('Helvetica', 20), pady=12)
        self.__player_text.pack()

    # Fonction de débug : affichage du board dans la console
    def debug_print_board(self):
        print("----------[ BOARD ]----------")
        for line in self.__board:
            print(line)

    def parameters_are_valid(self, board, victory):
        if board < 8 or board > 12:
            return False
        if victory < 4 or victory > 6:
            return False
        return True

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
            self.__board[coordinates["y"]][coordinates["x"]] = "."
            self.__pawns[self.__current_player] = Pawn((coordinates["x"], coordinates["y"]), self.__current_player)
            shape=self.__canvas.create_oval(coordinates["x"]*50+30,coordinates["y"]*50+30,coordinates["x"]*50+70,coordinates["y"]*50+70, fill=self.__colors["pawns"][self.__current_player], width=0)
            self.__shapes[self.__current_player] = shape
            self.__round += 1
            self.switch_player()
            self.debug_print_board()
            return

        if self.__round > 2:
            # Déplacement des pions
            pawn = self.__pawns[self.__current_player]
            if pawn.can_move_to((coordinates["x"], coordinates["y"]), self.__board, self.__board_length):
                pawn.move((coordinates["x"], coordinates["y"]), self.__board)
                self.__round += 1
                self.switch_player()
                self.debug_print_board()
            
            

    def run(self):
        self.__root.mainloop()

game=Game(True)
game.run()
