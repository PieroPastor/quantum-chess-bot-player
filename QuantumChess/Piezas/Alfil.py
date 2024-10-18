from Pieza import *

class Alfil(Pieza):
    def __init__(self, color, pos):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'B'
            self.valorPieza = 3
            self.CargaMovimiento()
        else: raise NotImplementedError

    def CargaMovimiento(self):
        for i in range(1, 8):
            self.movimientos.append((i, i))  # diagonal derecha abajo
            self.movimientos.append((-1 * i, i))  # diagonal izquierda abajo
            self.movimientos.append((i, -1 * i))  # diagonal derecha arriba
            self.movimientos.append((-1 * i, -1 * i))  # diagonal izquierda arriba