from .Pieza import *

class Caballo(Pieza):
    def __init__(self, color, pos):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'K'
            self.valorPieza = 3
            self.CargaMovimiento()
        else: raise NotImplementedError

    def CargaMovimiento(self):
        self.movimientos.append((2, 1))
        self.movimientos.append((2, -1))
        self.movimientos.append((-2, 1))
        self.movimientos.append((-2, -1))
        self.movimientos.append((1, 2))
        self.movimientos.append((1, -2))
        self.movimientos.append((-1, 2))
        self.movimientos.append((-1, -2))

    def CaminoOcupado(self, origen, objetivo, tablero):
        return False #El caballo no necesita la evaluación