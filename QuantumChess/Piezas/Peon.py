from .Pieza import *

class Peon(Pieza):
    def __init__(self, color, pos, avance):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'P'
            self.valorPieza = 1
            self.avance = avance #Donde avanza, si está abajo es -1, si está arriba es 1
            self.CargaMovimiento()
        else: raise NotImplementedError

    def CargaMovimiento(self):
        if self.color == BColors.WHITE:
            self.movimientos.append((-1, 0))  # Avance
            self.movimientos.append((-1, 1))  # Abajo derecha (come pieza contraria)
            self.movimientos.append((-1, -1))  # Abajo izquierda(come pieza contraria)
            self.movimientos.append((-2, 0))  # Avance
        if self.color == BColors.BLACK:
            self.movimientos.append((2, 0))  # Avance
            self.movimientos.append((1, 0))  # Avance
            self.movimientos.append((1, 1))  # arriba derecha (come pieza contraria)
            self.movimientos.append((1, -1))  # arriba izquierda (come pieza contraria)

    def RegistrarMovimiento(self, origen, objetivo):
        super().RegistrarMovimiento(origen, objetivo)
        if self.contadorMovimientos == 1:
            for mov in self.movimientos:
                yM, xM = mov
                if yM == 2 or yM == -2: self.movimientos.remove((yM, xM))

    def EvaluarPaso(self, origen, objetivo, tablero):
        xA, yA = origen
        xO, yO = objetivo
        if self.color == BColors.WHITE and yA == yO == tablero.peon_paso[0]: return True
        if self.color == BColors.BLACK and yA == yO == tablero.peon_paso[1]: return True
        return False

    def MovimientoValido(self, tablero, origen, objetivo):
        fila, columna = objetivo
        yA, xA = origen
        if fila-yA != self.avance and fila-yA != 0: return False #Si no avanza, o come al paso es invalido
        ultima_Pieza_mov = tablero.registro[-1] if tablero.registro else None
        x, y = (-1, -1)
        if ultima_Pieza_mov: y, x = ultima_Pieza_mov[2]
        if 0 <= fila < 8 and 0 <= columna < 8:  # Verifica si está dentro de los límites del tablero
            destino = tablero[fila][columna]
            if self.CaminoOcupado(origen, objetivo, tablero): return False
            if yA == fila and abs(xA-columna) == 1 and self.EvaluarPaso(origen, objetivo, tablero): return True
            if abs(fila-yA) == 1 and abs(xA-columna) == 1 and destino != '.': #Va a comer a otra pieza
                if self.color == BColors.WHITE: return BColors.BLACK in destino
                if self.color == BColors.BLACK: return BColors.WHITE in destino
            if abs(fila-yA) == 1 and xA-columna == 0 and destino == '.': return True #Va a avanzar
        return False