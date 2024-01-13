# 1ALGO
 Projet pour le chapitre de 1ALGO

## Documentation
<ul>
    <li><a href="#class_pawn">La classe Pawn</a></li>
    <li><a href="#class_game">La classe Game</a></li>
</ul>

---

<div id="class_pawn"></div>

### La classe Pawn
La classe Pawn représente le pion d'un joueur situé sur le plateau.

__Attributs :__
- coordinates -> list, inclut les coordonnées x et y du joueur
- player -> int, numéro du joueur (0 ou 1)

__Fonctions et procédures :__
- get_coordinates() -> fonction renvoyant les coordonnées du joueur dans un tuple.
- get_player() -> fonction renvoyant le numéro du joueur correspondant au pion.
- can_move_to((x,y), board, board_length) -> fonction renvoyant True si le joueur peut déplacer son pion aux coordonnées x et y du tuple renseigné en entrée et False si ce n'est pas le cas.
- is_stuck(board, board_length) -> fonction renvoyant True si le joueur ne peut plus déplacer son pion et False dans le cas inverse.
- move((x,y), board) -> fonction faisant bouger le pion du joueur aux coordonnées x et y du tuple renseigné en entrée, en partant de l'idée que le déplacement vers (x,y) est possible et vérifié par `can_move_to()`. Laisser une marque sur le plateau une fois le déplacement terminé. Retourne les coordonnées d'origine pour placer une marque sur le plateau.

<div id="class_game"></div>

### La classe Game
Game correspond à la partie en cours. La classe gère l'interface utilisateur, les paramètres de la partie et toute la logique du cycle de jeu.

__Attributs :__
- board_length -> int, taille du tableau en cases
- board -> list, plateau de jeu stockant les valeurs de chaque case (vide, pion ou marque)
- root -> fenêtre Tkinter principale
- canvas, player_text -> éléments de l'interface graphique Tkinter (tableau et texte indiquant le joueur actif)
- win_length -> int, nombre de marques à aligner pour gagner la partie
- pawns -> list, contient les instances de la classe Pawn (pions des joueurs)
- shapes -> list, contient les cercles représentant les pions dans l'interface utilisateur afin de modifier leurs coordonnées au déplacement.
- colors -> dict, dictionnaire avec tous les paramètres de couleurs de l'interface graphique, incluant couleurs des pions et de l'interface graphique. Intégration future d'un mode sombre dans l'application
- player_var -> StringVar, gère l'affichage du joueur actif (via player_text)

__Fonctions et procédures :__
- parameters_are_valid(board, victory) -> fonction vérifiant si les paramètres passés en entrée sont conformes et retourne True si c'est le cas, sinon, retourne False.
- switch_player() -> procédure faisant la rotation entre les deux joueurs.
- get_square(x,y) -> fonction convertissant les coordonnées d'un click dans le canvas en coordonnées d'une case du plateau. Renvoie un dictionnaire contenant les coordonnées de la case du tableau.
- handle_click(event) -> fonction exécutée à chaque click (...)
- run() -> procédure chargée de lancer le jeu.
