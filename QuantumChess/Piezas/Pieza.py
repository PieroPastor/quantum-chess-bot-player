from Utils import *
from .BColors import BColors

class Pieza:
    def __init__(self, color, pos):
        self.color = color #Color de la pieza
        self.simbolo = ' ' #Simbolo de la pieza de ajedrez
        self.posiciones = [pos] #Posiciones ocupadas por la pieza
        self.movimientos = [] #Movimientos posibles de la pieza
        self.estaVivo = True #Indica si la pieza sigue viva
        self.contadorMovimientos = 0 #Veces en la que la pieza se movio
        self.valorPieza = 0 #Valor de la pieza en el juego

    def RegistrarMovimiento(self, origen, objetivo):
        self.posiciones[self.posiciones.index(origen)] = objetivo
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
                if tablero[yA][xA+((xO < xA)*-1)*2*i+i] != '.': return True
        elif xA-xO == 0:
            aux = abs(yA - yO)
            for i in range(1, aux):
                if tablero[yA+((yO < yA)*-1)*2*i+i][xA] != '.': return True
        else:
            distancia = int(math.sqrt((yA - yO) ** 2 + (xA - xO) ** 2))
            for i in range(1, distancia):
                if tablero[yA + ((yO < yA) * -1)*2*i+i][xA + ((xO < xA) * -1)*2*i+i] != '.': return True
        return False

    def MovimientoValido(self, tablero, origen, objetivo):
        fila, columna = objetivo
        yA, xA = origen
        if 0 <= fila < 8 and 0 <= columna < 8:  # Verifica si está dentro de los límites del tablero
            destino = tablero[fila][columna]  # Para saber si el destino está vacío
            if self.CaminoOcupado((yA, xA), objetivo, tablero): return False
            if destino == '.': return True
            if self.color == BColors.WHITE: return BColors.BLACK in destino
            if self.color == BColors.BLACK: return BColors.WHITE in destino
        return False

    def ReiniciarMovimientos(self, pos):
        self.posiciones = [pos]

    def EvaluarPaso(self, origen, objetivo, tablero):
        raise NotImplementedError

