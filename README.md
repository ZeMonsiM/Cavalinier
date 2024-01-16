# 1ALGO
 Projet Python pour le chapitre de 1ALGO.

## Documentation
<ul>
    <li><a href="#class_pawn">La classe Pawn</a></li>
    <li><a href="#class_game">La classe Game</a></li>
    <li><a href="#save_load_feature">Sauvegarde</a></li>
    <li><a href="#settings_guide">Guide de paramétrage</a></li>
    <li><a href="#default_settings">Paramètres par défaut</a></li>
    <li><a href="#color_themes">Thèmes de l'interface</a></li>
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
- move((x,y), board, canvas, shapes, colors) -> fonction faisant bouger le pion du joueur aux coordonnées x et y du tuple renseigné en entrée, en partant de l'idée que le déplacement vers (x,y) est possible et vérifié par `can_move_to()`. Laisser une marque sur le plateau une fois le déplacement terminé. Retourne les coordonnées d'origine pour placer une marque sur le plateau.

---

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
- check_board_for_alignment() -> procédure parcourant toutes les cases du plateau de jeu pour y trouver des marques laissées par les joueurs. Appelle la procédure `check_nearby_squares()` pour continuer la vérification.
- check_nearby_squares(player, (x,y)) -> procédure vérifiant si une marque du joueur existe autour des coordonnées spécifiées. Appelle la procédure `check_length()` pour vérifier si d'autres marques sont alignées.
- check_length((x,y), player, length, direction) -> procédure récursive vérifiant la longueur d'un alignement de marques du joueur. `check_length()` vérifie dans une direction précise donnée par la procédure `check_nearby_squares()` et incrémente `length` à chaque marque trouvée, jusqu'à ce que la condition de victoire soit satisfaite.
- victory(reason) -> procédure affichant un message de victoire et mettant fin à la partie.
- clear_interface() -> procédure chargée de réinitialiser le plateau du côté de l'interface graphique, en supprimant toutes les marques.
- reset() -> procédure qui réinitialise la partie en cours lorsque le joueur clique sur "Réinitialiser" dans le menu du jeu.
- save_game() -> procédure enregistrant les informations de la partie en cours dans un fichier `save.json`.
- load_game() -> procédure qui charge les informations de la partie sauvegardée dans `save.json`.
- run() -> procédure chargée de lancer le jeu.

---

<div id="save_load_feature"></div>

### Fonction de sauvegarde de partie
Le jeu intègre une fonction de sauvegarde de la partie en cours pour les parties les plus longues. Le fichier de sauvegarde est écrit en JSON afin de conserver facilement les données dans un format lisible aussi bien par l'humain que par la machine.
La sauvegarde est enregistrée sous la forme suivante :
```json
{
    "players": [
        {
            "name": "Player Name",
            "color": "#FF0000",
            "x": 0,
            "y": 0
        },
        {
            "name": "Player Name",
            "color": "#0000FF",
            "x": 5,
            "y": 5
        }
    ],
    "board": [[],[],[],[],[]]
}
```

---

<div id="settings_guide"></div>

### Comment paramétrer le jeu ?
> Le jeu dispose de plusieurs paramètres, dont les paramètres par défaut et le thème de l'interface. Ces paramètres sont passés dans la classe Game lors de son initialisation. Voici la liste des paramètres :
```
Game(<paramètres par défaut>, <thème de l'interface>)
```

Par exemple, si l'utilisateur souhaite utiliser les paramètres par défaut pour ne pas avoir à entrer les valeurs manuellement, il peut modifier le code de cette façon :
```python
game=Game(True)
```
Si l'utilisateur veut utiliser un thème sombre sans utiliser les paramètres par défaut, il peut utiliser ce code :
```python
game=Game(False, "dark")
```
> A terme, un fichier `options.txt` est prévu pour y entrer les paramètres de jeu sans avoir à modifier le code du jeu. Cette mise à jour est prévue pour plus tard...

---

<div id="default_settings"></div>

### Paramètres par défaut
> Une partie peut être forcée avec les paramètres par défaut en spécifiant `True` lors de la création de l'instance de Game. Une grille de 10x10 sera alors utilisée et 5 marques devront être alignées pour déclencher la victoire par alignement.

---

<div id="color_themes"></div>

### Thèmes de l'interface
> L'interface du jeu est disponible sous deux thèmes de couleurs : un mode clair et un mode foncé. Par défaut, le mode clair est sélectionné, mais l'utilisateur peut spécifier dans le deuxième argument de la classe Game le thème qu'il souhaite utiliser pour l'interface