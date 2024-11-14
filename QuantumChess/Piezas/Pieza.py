import math
import sys
import cirq
import copy
import random
import matplotlib.pyplot as plt
import numpy as np
from .BColors import BColors

class Pieza:
    def __init__(self, color, pos):
        self.color = color #Color de la pieza
        self.simbolo = ' ' #Simbolo de la pieza de ajedrez
        self.posiciones = [pos] #Posiciones ocupadas por la pieza
        self.historial = [pos] #Lugares por donde pasó
        self.movimientos = [] #Movimientos posibles de la pieza
        self.entrelazadas = [] #Guardará el índice de las piezas con las que se entrelazó
        self.estaVivo = True #Indica si la pieza sigue viva
        self.contadorMovimientos = 0 #Veces en la que la pieza se movio
        self.valorPieza = 0 #Valor de la pieza en el juego

    def RegistrarMovimiento(self, origen, objetivo):
        if origen in self.posiciones: self.posiciones[self.posiciones.index(origen)] = objetivo
        else: self.posiciones.append(objetivo)
        if objetivo not in self.historial: self.historial.append(objetivo)
        self.contadorMovimientos += 1

    def CargaMovimiento(self):
        raise NotImplementedError

    def PuedeCapturar(self, pieza):
        return isinstance(pieza, Pieza) and self.color != pieza.color

    @staticmethod
    def Ruta(mov):
        yA, xA = mov

        if yA < 0: yA = -1
        elif yA > 0: yA = 1
        if xA < 0: xA = -1
        elif xA > 0: xA = -1

        return yA, xA

    def CaminoOcupado(self, origen, objetivo, tablero):
        yA, xA = origen
        yO, xO = objetivo
        if yA-yO == 0:
            aux = abs(xA - xO)
            for i in range(1, aux):
                auxX = xA + ((xO < xA) * -1) * 2 * i + i
                if auxX == xO: return False
                if tablero[yA][auxX] != '.': return True
        elif xA-xO == 0:
            aux = abs(yA - yO)
            for i in range(1, aux):
                auxY = yA + ((yO < yA) * -1) * 2 * i + i
                if auxY == yO: return False
                if tablero[auxY][xA] != '.': return True
        else:
            distancia = int(math.sqrt((yA - yO) ** 2 + (xA - xO) ** 2))
            for i in range(1, distancia):
                auxY = yA + ((yO < yA) * -1) * 2 * i + i
                auxX = xA + ((xO < xA) * -1) * 2 * i + i
                if auxX == xO and auxY == yO: return False
                if 0 <= auxY < 8 and 0 <= auxX < 8 and tablero[auxY][auxX] != '.': return True
        return False

    def MovimientoValido(self, tablero, origen, objetivo, necesita_camino=True, auxPeon=None):
        try: tablero = tablero.tablero
        except: tablero = tablero
        fila, columna = objetivo
        yA, xA = origen
        if 0 <= fila < 8 and 0 <= columna < 8:  # Verifica si está dentro de los límites del tablero
            destino = tablero[fila][columna]  # Para saber si el destino está vacío
            if necesita_camino and self.CaminoOcupado((yA, xA), objetivo, tablero): return False
            if destino == '.': return True
            if self.color == BColors.WHITE: return BColors.BLACK in destino
            if self.color == BColors.BLACK: return BColors.WHITE in destino
        return False

    def ReiniciarMovimientos(self, pos):
        self.posiciones = [pos]

    def EvaluarPaso(self, origen, objetivo, tablero, peon_paso=None):
        raise NotImplementedError

