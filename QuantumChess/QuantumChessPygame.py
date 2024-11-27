from Pantallas import *
from Tablero import Tablero

# Ejecutar el menú y el juego
while True:
    game_mode, color = main_menu()
    # Tablero por defecto
    default_board = Tablero()
    if game_mode: main_player(default_board) # Juego 1 vs 1
    else: main_ai(default_board, color) # Juego 1 vs Máquina
