from tkinter import *
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter.colorchooser import askcolor
from os.path import exists
from random import randint
import json

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
        x,y = self.__coordinates[0], self.__coordinates[1]
        if x < board_length - 1 and y > 1 and board[y-2][x+1] == None:
            return False
        if x < board_length - 2 and y > 0 and board[y-1][x+2] == None:
            return False
        if x < board_length - 2 and y < board_length - 1 and board[y+1][x+2] == None:
            return False
        if x < board_length - 1 and y < board_length - 2 and board[y+2][x+1] == None:
            return False
        if x > 0 and y < board_length - 2 and board[y+2][x-1] == None:
            return False
        if x > 1 and y < board_length - 1 and board[y+1][x-2] == None:
            return False
        if x > 1 and y > 0 and board[y-1][x-2] == None:
            return False
        if x > 0 and y > 1 and board[y-2][x-1] == None:
            return False
        return True

    def move(self, coordinates: tuple, board, canvas, shapes, colors):
        old_coordinates = self.__coordinates
        self.__coordinates = [coordinates[0], coordinates[1]] # Changement des coordonnées
        board[old_coordinates[1]][old_coordinates[0]] = self.__player # Rajouter la marque du joueur
        board[self.__coordinates[1]][self.__coordinates[0]] = "." # Déplacer le pion dans le board
        
        canvas.create_line(old_coordinates[0]*50+35,old_coordinates[1]*50+35,old_coordinates[0]*50+65,old_coordinates[1]*50+65,width=3,fill=colors["pawns"][self.__player])
        canvas.create_line(old_coordinates[0]*50+65,old_coordinates[1]*50+35,old_coordinates[0]*50+35,old_coordinates[1]*50+65,width=3,fill=colors["pawns"][self.__player])
        canvas.move(shapes[self.__player], (self.__coordinates[0]-old_coordinates[0])*50, (self.__coordinates[1]-old_coordinates[1])*50)


# Classe Game
# Gère toute la logique du jeu.
# Attributs : board_length, board, root (+ autres éléments de l'interface graphique), win_length, pawns, colors, player_var
# Méthodes : run, get_square, handle_click, switch_player, parameters_are_valid, victory_by_align, victory
class Game():
    def __init__(self):
        settings = self.load_settings()
        use_default_values = settings['use_default_settings']
        use_custom_colors = settings['use_custom_colors']
        use_custom_names = settings['use_custom_names']
        self.__ui_theme = settings['theme']

        if not use_default_values:
            self.__board_length = askinteger("Jeu","Quelle est la taille du plateau (entre 8 et 12) ?")
            self.__win_length = askinteger("Jeu","Nombre de marques à aligner pour gagner (entre 4 et 6) ?")
            self.__multiplayer = askyesno("Jeu","Voulez vous jouer en multijoueur ?")

            if not self.parameters_are_valid(self.__board_length, self.__win_length):
                showerror("Erreur","Les paramètres de jeu sont incorrects ! Veuillez vérifier que la taille du plateau et que la condition de victoire soient bien configurées et réessayez.")
                exit()
        else:
            self.__board_length = 10
            self.__win_length = 5
            self.__multiplayer = True
        
        self.__player_names = [None, None]
        if use_custom_names:
            players = 2 if self.__multiplayer else 1
            for i in range(players):
                self.__player_names[i] = askstring("Jeu",f"Joueur {i + 1} : Entrez votre pseudo...")

        self.__colors={
                "pawns": ["red","blue"],
                "interface": {
                    "light": {
                        "background": "#FFFFFF",
                        "foreground": "#000000"
                    },
                    "dark": {
                        "background": "#222222",
                        "foreground": "#FFFFFF"
                    }
                }
        }
        if use_custom_colors:
            players = 2 if self.__multiplayer else 1
            for i in range(players):
                self.__colors['pawns'][i] = askcolor(title=f"Joueur {i + 1} : Choisissez votre couleur")[1]

        self.__board = [[None for i in range(self.__board_length)] for j in range(self.__board_length)]
        self.__pawns = [None, None]
        self.__shapes = [None, None]
        self.__round = 1
        self.__current_player = 0

        self.__root=Tk()
        self.__root.resizable(False, False)
        self.__root.title("Jeu")

        menu = Menu(self.__root)
        self.__root.config(menu=menu)
        menu.add_command(label="Réinitialiser", command=self.reset)
        menu.add_command(label="Sauvegarder", command=self.save_game)
        menu.add_command(label="Charger", command=self.load_game)
        menu.add_command(label="Quitter", command=exit)
        
        self.__canvas=Canvas(self.__root, width=50*self.__board_length+50, height=50*self.__board_length+50)
        self.__canvas.bind("<Button-1>", self.handle_click)
        self.__canvas.pack()

        for i in range(self.__board_length+1):
            self.__canvas.create_line(25+i*50,25,25+i*50,25+50*self.__board_length)
            self.__canvas.create_line(25,25+i*50,25+50*self.__board_length,25+i*50)

        self.__round_var = StringVar()
        self.__round_var.set("Round "+str(self.__round))
        self.__round_text=Label(self.__root, textvariable=self.__round_var, font=('Helvetica', 15))
        self.__round_text.pack()

        self.__player_var = StringVar()
        self.__player_var.set(self.__player_names[self.__current_player]) if self.__player_names[self.__current_player] else self.__player_var.set("Joueur 1")
        self.__player_text=Label(self.__root, textvariable=self.__player_var, font=('Helvetica', 20), pady=12)
        self.__player_text.pack()
    
    def load_settings(self):
        if not exists('options.json'):
            showinfo("Jeu","Le fichier 'options.json' est introuvable. Création du fichier avec les paramètres par défaut...")
            with open('options.json','w') as settings_file:
                settings = {
                    "use_default_settings": True,
                    "theme": "light",
                    "use_custom_colors": True,
                    "use_custom_names": True
                }
                json_string = json.dumps(settings, indent=2)
                settings_file.write(json_string)
            return settings
        
        with open('options.json','r') as settings_file:
            settings = json.loads(settings_file.read())
        
        return settings

    # Fonction de débug : affichage du board dans la console
    def debug_print_board(self):
        print("----------[ BOARD ]----------")
        for line in self.__board:
            print(line)

    def parameters_are_valid(self, board, victory):
        if not board or not victory:
            return False
        if board < 8 or board > 12:
            return False
        if victory < 4 or victory > 6:
            return False
        return True

    def switch_player(self):
        self.__current_player = (self.__current_player + 1) %2
        self.__player_var.set(self.__player_names[self.__current_player]) if self.__player_names[self.__current_player] else self.__player_var.set(f"Joueur {self.__current_player + 1}")

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
            self.__round_var.set("Round "+str(self.__round))
            self.switch_player()
            if not self.__multiplayer:
                self.play_ai()
            return

        if self.__round > 2:
            # Déplacement des pions
            pawn = self.__pawns[self.__current_player]
            if pawn.can_move_to((coordinates["x"], coordinates["y"]), self.__board, self.__board_length):
                pawn.move((coordinates["x"], coordinates["y"]), self.__board, self.__canvas, self.__shapes, self.__colors)
                self.__round += 1
                self.__round_var.set("Round "+str(self.__round))
                self.switch_player()
                other_pawn = self.__pawns[self.__current_player] # Joueur modifié par switch_player, le pion adverse est donc sélectionné
                if other_pawn.is_stuck(self.__board, self.__board_length):
                    self.switch_player()
                    self.victory("Le joueur adverse est bloqué")
                self.check_board_for_alignment()
                if not self.__multiplayer:
                    self.play_ai()
                return
            
    def check_board_for_alignment(self):
        for line in range(self.__board_length):
            for column in range(self.__board_length):
                if self.__board[line][column] == 0 or self.__board[line][column] == 1:
                    self.check_nearby_squares(self.__board[line][column], (column, line))

    def check_nearby_squares(self, player, coordinates: tuple):
        x,y = coordinates[0], coordinates[1]
        if y > 0 and self.__board[y-1][x] == player:
            self.check_length(coordinates, player, 1, "top")
        if x < self.__board_length -1 and y > 0 and self.__board[y-1][x+1] == player:
            self.check_length(coordinates, player, 1, "top_right")
        if x < self.__board_length -1 and self.__board[y][x+1] == player:
            self.check_length(coordinates, player, 1, "right")
        if x < self.__board_length -1 and y < self.__board_length -1 and self.__board[y+1][x+1] == player:
            self.check_length(coordinates, player, 1, "bottom_right")
        if y < self.__board_length -1 and self.__board[y+1][x] == player:
            self.check_length(coordinates, player, 1, "bottom")
        if x > 0 and y < self.__board_length -1 and self.__board[y+1][x-1] == player:
            self.check_length(coordinates, player, 1, "bottom_left")
        if x > 0 and self.__board[y][x-1] == player:
            self.check_length(coordinates, player, 1, "left")
        if x > 0 and y > 0 and self.__board[y-1][x-1] == player:
            self.check_length(coordinates, player, 1, "top_left")

    def check_length(self, coordinates: tuple, player, length, direction):
        x,y = coordinates[0], coordinates[1]
        board_length = self.__board_length
        board = self.__board
        conditions = {
            "top": "y > 0 and board[y-1][x] == player",
            "top_right": "x < board_length -1 and y > 0 and board[y-1][x+1] == player",
            "right": "x < board_length -1 and board[y][x+1] == player",
            "bottom_right": "x < board_length -1 and y < board_length -1 and board[y+1][x+1] == player",
            "bottom": "y < board_length -1 and board[y+1][x] == player",
            "bottom_left": "x > 0 and y < board_length -1 and board[y+1][x-1] == player",
            "left": "x > 0 and board[y][x-1] == player",
            "top_left": "x > 0 and y > 0 and board[y-1][x-1] == player"
        }
        new_coordinates = {
            "top": (x,y-1),
            "top_right": (x+1,y-1),
            "right": (x+1,y),
            "bottom_right": (x+1,y+1),
            "bottom": (x,y+1),
            "bottom_left": (x-1,y+1),
            "left": (x-1,y),
            "top_left": (x-1,y-1)
        }

        if length >= self.__win_length:
            self.switch_player()
            player_name = self.__player_names[player] if self.__player_names[player] else player + 1
            self.victory(f"{self.__win_length} marques ont été alignées par le joueur {player_name}.")
        
        if eval(conditions[direction]):
            self.check_length(new_coordinates[direction], player, length + 1, direction)

    def victory(self, reason):
        player = self.__player_names[self.__current_player] if self.__player_names[self.__current_player] else self.__current_player + 1
        showinfo("Victoire !",f"Le joueur {player} a gagné la partie !\n{reason}")
        exit()
    
    def clear_interface(self):
        self.__canvas.delete('all')
        for i in range(self.__board_length+1):
            self.__canvas.create_line(25+i*50,25,25+i*50,25+50*self.__board_length)
            self.__canvas.create_line(25,25+i*50,25+50*self.__board_length,25+i*50)
    
    def reset(self):
        # Réinitialiser le plateau
        self.__board = [[None for i in range(self.__board_length)] for j in range(self.__board_length)]

        # Réinitialiser les pions des joueurs et le joueur actif
        self.__pawns = [None, None]
        self.__shapes = [None, None]
        self.__round = 1
        self.__current_player = 0

        # Réinitialiser l'interface graphique
        self.clear_interface()
    
    def save_game(self):
        json_string = json.dumps({
            "players": [
                {
                    "name": self.__player_names[0],
                    "color": self.__colors["pawns"][0],
                    "x": self.__pawns[0].get_coordinates()[0],
                    "y": self.__pawns[0].get_coordinates()[1]
                },
                {
                    "name": self.__player_names[1],
                    "color": self.__colors["pawns"][1],
                    "x": self.__pawns[1].get_coordinates()[0],
                    "y": self.__pawns[1].get_coordinates()[1]
                }
            ],
            "board": self.__board,
            "win_length": self.__win_length,
            "current_player": self.__current_player,
            "round": self.__round
        }, indent=2)
        with open('save.json','w') as save_file:
            save_file.write(json_string)

    def load_game(self):
        if not exists("save.json"):
            showerror("Charger","Il n'y a pas de fichier de sauvegarde disponible !")
        
        with open('save.json','r') as save_file:
            json_string = json.loads(save_file.read())
        
        # Charger les données de la sauvegarde
        self.__board = json_string['board']
        self.__board_length = len(self.__board)
        self.__win_length = json_string['win_length']
        self.__current_player = json_string['current_player']
        self.__round = json_string['round']
        self.__player_var.set(f"Joueur {self.__current_player + 1}")

        self.clear_interface()
        self.__canvas.config(width=50*self.__board_length+50, height=50*self.__board_length+50)
        self.__root.geometry(f"{50*self.__board_length+50}x{50*self.__board_length+100}")

        for player in range(2):
            # Données des joueurs
            self.__colors['pawns'][player] = json_string['players'][player]['color']
            self.__player_names[player] = json_string['players'][player]['name']
            self.__pawns[player] = Pawn((json_string['players'][player]['x'], json_string['players'][player]['y']), player)
            self.__shapes[player] = self.__canvas.create_oval(json_string['players'][player]['x']*50+30,json_string['players'][player]['y']*50+30,json_string['players'][player]['x']*50+70,json_string['players'][player]['y']*50+70, fill=self.__colors["pawns"][player], width=0)

        # Redessiner le plateau depuis la sauvegarde
        for y in range(self.__board_length):
            for x in range(self.__board_length):
                if type(self.__board[y][x]) == int:
                    # Marque détectée, dessiner la marque
                    self.__canvas.create_line(x*50+35,y*50+35,x*50+65,y*50+65,width=3,fill=self.__colors["pawns"][self.__board[y][x]])
                    self.__canvas.create_line(x*50+65,y*50+35,x*50+35,y*50+65,width=3,fill=self.__colors["pawns"][self.__board[y][x]])

    def play_ai(self):
        pawn = self.__pawns[self.__current_player]
        valid_move = False
        if not pawn:
            # Premier tour
            while not valid_move:
                x,y = randint(0, self.__board_length - 1), randint(0, self.__board_length - 1)
                valid_move = True if self.__board[y][x] == None else False
            self.__board[y][x] = "."
            self.__pawns[self.__current_player] = Pawn((x, y), self.__current_player)
            shape=self.__canvas.create_oval(x*50+30,y*50+30,x*50+70,y*50+70, fill=self.__colors["pawns"][self.__current_player], width=0)
            self.__shapes[self.__current_player] = shape
            self.__round += 1
            self.__round_var.set("Round "+str(self.__round))
            self.switch_player()
            return

        # Déplacement de pion
        coordinates = pawn.get_coordinates()
        x,y = coordinates[0], coordinates[1]
        destinations = [
            (x+1,y-2),
            (x+2,y-1),
            (x+2,y+1),
            (x+1,y+2),
            (x-1,y+2),
            (x-2,y+1),
            (x-2,y-1),
            (x-1,y-2)
        ]

        while not valid_move:
            selected_destination = destinations[randint(0,7)]
            valid_move = pawn.can_move_to(selected_destination, self.__board, self.__board_length)

        pawn.move(selected_destination, self.__board, self.__canvas, self.__shapes, self.__colors)
        self.__round += 1
        self.__round_var.set("Round "+str(self.__round))
        self.switch_player()
        other_pawn = self.__pawns[self.__current_player] # Joueur modifié par switch_player, le pion adverse est donc sélectionné
        if other_pawn.is_stuck(self.__board, self.__board_length):
            self.switch_player()
            self.victory("Le joueur adverse est bloqué")

    def run(self):
        self.__root.mainloop()

game=Game()
game.run()
