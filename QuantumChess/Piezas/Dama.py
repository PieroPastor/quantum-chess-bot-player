from .Pieza import *

class Dama(Pieza):
    def __init__(self, color, pos):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'Q'
            self.valorPieza = 9
            self.CargaMovimiento()
        else: raise NotImplementedError

    def CargaMovimiento(self):
        for i in range(1, 8):
            self.movimientos.append((i, i))  # diagonal derecha abajo
            self.movimientos.append((-1 * i, i))  # diagonal izquierda abajo
            self.movimientos.append((i, -1 * i))  # diagonal derecha arriba
            self.movimientos.append((-1 * i, -1 * i))  # diagonal izquierda arriba
            self.movimientos.append((i, 0))  # avanza a la derecha de A a H
            self.movimientos.append((-1 * i, 0))  # Avanza a la izquierda de H a A
            self.movimientos.append((0, i))  # avanza a la abajo de A a H
            self.movimientos.append((0, -1 * i))  # Avanza a la arriba de H a A