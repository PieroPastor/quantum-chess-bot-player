import sys
sys.path.append('quantum-chess-bot-player/QuantumChess')  # Ajusta la ruta si es necesario
import Tablero
import Piezas
from Piezas import BColors
import csv
##################################
from collections import namedtuple
from Tablero import Tablero
import random
import itertools
import copy
import sys
import threading
import pickle


"""## Clase Juego"""

class Game:
  def actions(self, state):
    """Retorna una lista de movidas permitidas en el estado actual state."""
    raise NotImplementedError

  def result(self, state, move):
    """Retorna el nuevo estado que resulta de hacer una movida move en el estado state."""
    raise NotImplementedError

  def utility(self, state, player):
    """Retorna el valor de utilidad para el jugador player en el estado terminal state."""
    raise NotImplementedError

  def terminal_test(self, state):
    """Retorna True si el estado state es un estado terminal del juego."""
    return not self.actions(state)

  def to_move(self, state):
    """Retorna el jugador que le toca jugar en el presente estado state."""
    return state.to_move

  def display(self, state):
    """Imprime o displaya el state."""
    print(state)

  def __repr__(self):
    return '<{}>'.format(self.__class__.__name__)

  def move_thread(self, state, player):
    try:
      move = player(self, state)
      mark_now = self.to_move(state)
      state = self.result(state, move)
    except Exception:
      return

  def states_generator(self, *players, verbose=False):
    """Controlador del juego:
    Llama alternadamente a cada jugador pasandole el estado actual del juego y ejecutando la movida retornada."""
    state = self.initial
    numJugada = 0
    states_created = []
    states_created.append(state)
    while True:
      for player in players:
        hilo = threading.Thread(target=self.move_thread, args=(state, player))
        hilo.start()
        hilo.join(timeout=5) #5 segundos de tiempo limite para un movimiento random
        if hilo.is_alive(): #Sigue generando y no debería pues es aleatorio
          return states_created #Retorna lo que ha podido crear
        try:
          move = player(self, state)
          mark_now = self.to_move(state)
          state = self.result(state, move)
        except Exception:
          return states_created
        numJugada = numJugada + 1
        if self.terminal_test(state):
          return states_created
        states_created.append(state)

  def convert_pieces(self, board):
    tablero = board.tablero
    probabilidades = board.probabilidades
    t = []
    for row in tablero:
      for i in row:
        if i == ".": t.append(0)
        else:
          p = i[5]
          if i[0:5] == BColors.BLACK: mult = -1
          else: mult = 1
          t.append(ord(p)*mult)
    return t
    for row in probabilidades:
      for i in row:
        t.append(i)

  def convert_move(self, move):
    neo = [move[0]]
    for i in range(1, 5):
      if not isinstance(move[i], int): neo.append(move[i][0]*8+move[i][1])
      else: neo.append(-1)
    neo.append(move[5])
    return neo

"""##QuantumChess Class"""

#Para este entorno, un estado es una tupla con nombres de campos (namedtuple)
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class QuantumChess(Game):
  def __init__(self):
    self.tab = Tablero()
    moves = self.tab.GetMoves('W')
    self.initial = GameState(to_move='W', utility=0, board=self.tab, moves=moves)

  #Cargará los movimientos posibles para el que le toque, si es white, le toca a black
  def update_movements(self, state):
    #print(state.board.GetMoves('W' if state.to_move == 'B' else 'B'))
    return state.board.GetMoves('W' if state.to_move == 'B' else 'B')

  #No da los movimientos necesariamente posibles, sino da los disponibles por pieza.
  #Esto porque la funcion GenericMove se encarga de analizarlos
  def actions(self, state):
    "Retorna moves porque estate es de la tupla GameState"
    return state.moves

  def result(self, state, move):
    if move not in state.moves: return state #No hay cambios
    board = state.board.Clon()
    board.GenericMove(move)
    moves = self.update_movements(state)
    return GameState(to_move=('W' if state.to_move == 'B' else 'B'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

  def utility(self, state, player):
    """Retorna la utilidad del player en estado terminal state; 1 si ganó, -1 si perdió, 0 empate."""
    if player == 'W': return state.board.puntaje_blancas - state.board.puntaje_negras
    if player == 'B': return state.board.puntaje_negras - state.board.puntaje_blancas

  def terminal_test(self, state):
    """Un estado es terminal si hay un ganador o no hay mas movidas posibles."""
    return len(state.moves) == 0

  def display(self, state):
    board = state.board
    board.ImprimirTablero()

  def compute_utility(self, board, move, player):
    if player == 'W': return board.puntaje_blancas - board.puntaje_negras
    if player == 'B': return board.puntaje_negras - board.puntaje_blancas

"""## Algoritmo Monte Carlo

Implementación del Nodo
"""

class MCT_Node:
  """Nodo del árbol de búsqueda Monte Carlo. Hace un seguimiento de los estados hijos (`children` states)."""
  def __init__(self, parent=None, state=None, U=0, N=0):
    self.__dict__.update(parent=parent, state=state, U=U, N=N)
    self.children = {} #No hay hijos al inicio
    self.actions = None

"""Implementación de la función UCB1 para la selección. (Límite de confianza superior)"""

import numpy as np
#Función donde n es el nodo y C es una constante
#n.parent.N es el total de simulaciones, y
def ucb(n, C=1.4):
  """Función UCB para la fase de selección."""
  if n.N == 0: return np.inf
  else: return (n.U / n.N) + C * np.sqrt(np.log(n.parent.N) / n.N)

"""Algoritmo MCTS"""

import random

#N es la cantidad de simulaciones
def monte_carlo_tree_search(state, game, N=20, m=20):
  def select(n):
    """Selecciona un nodo del árbol."""
    if n.children: return select(max(n.children.keys(), key=ucb)) #Retorna el mejor nodo
    else: return n #Si no hay hijos se retorna a sí mismo

  def expand(n):
    """Expande la rama agregando todos sus estados hijo"""
    if not n.children and not game.terminal_test(n.state): #Si el juego no se acabó
      n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                    for action in game.actions(n.state)} #Crea un hijo por accion posible
    return select(n)

  def simulate(game, state):
    """Simula la utilidad del estado actual al tomar aleatoriamente un paso."""
    player = game.to_move(state)
    i = 0 #Contador de iteraciones (para medir profundidad)
    while not game.terminal_test(state) and i < m: #Mientras que no se acabe
      action = random.choice(list(game.actions(state))) #Elige una accion aleatoria
      state = game.result(state, action)
      if game.terminal_test(state) and state.to_move == player: return -1000 #Hizo jaque mate
      elif game.terminal_test(state): return 1000 #Le hicieron jaque mate
      i += 1
    #print(player, game.utility(state, player), state.board.puntaje_blancas, state.board.puntaje_negras, action)
    v = game.utility(state, player)
    return -v #Retorna la puntuación en negativo, porque la recibirá min

  def backprop(n, utility):
    """Pasa la utilidad a todos los nodos padre (es decir, hacia atrás)."""
    if utility > 0: n.U += utility
    n.N += 1
    if n.parent: backprop(n.parent, -utility)

  root = MCT_Node(state=state)

  for _ in range(N): #Se expande N veces
    leaf = select(root)
    child = expand(leaf)
    result = simulate(game, child.state)
    backprop(child, result)

  max_state = max(root.children, key=lambda p: p.U)
  return root.children.get(max_state)

"""## Players"""

def mcts_player(game, state, n=20, m=20):
  return monte_carlo_tree_search(state, game, N=n, m=m)

def random_player(game, state):
  a = random.choice(game.actions(state))
  return a

"""## Game Simulator"""

random_states = []

if len(sys.argv) == 1: #Si no se le manda un pickle lo genera
  for i in range(50):
    qchess = QuantumChess()
    random_states += qchess.states_generator(random_player, random_player)

  print(sys.getsizeof(random_states), len(random_states))

  with open('states.pkl', 'wb') as archivo:
      pickle.dump(random_states, archivo)
else: #Si se le manda lo lee y en base a eso trabaja
  with open(sys.argv[1], 'rb') as archivo:
      random_states = pickle.load(archivo)
  print(sys.getsizeof(random_states), len(random_states))
  
  qchess = QuantumChess()
  random.shuffle(random_states)
  with open("dataset.csv", mode="w", newline="") as archivo:
    escritor_csv = csv.writer(archivo)
    print("LOADED")
    for state in random_states:
      try:
        if len(sys.argv) == 4: move = mcts_player(qchess, state, int(sys.argv[2]), int(sys.argv[3]))
        else: move = mcts_player(qchess, state)
        input_board = [1 if state.to_move == "W" else 0]
        input_board += qchess.convert_pieces(state.board)
        #mark_now = qchess.to_move(state) No se actualizará el movimiento
        #state = qchess.result(state, move) No necesitamos mover
        output_move = qchess.convert_move(move)
        escritor_csv.writerow(input_board+output_move)
      except Exception:
        pass
    archivo.close()

  print("FIN")
  
