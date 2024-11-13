from .Pieza import *

class Peon(Pieza):
    def __init__(self, color, pos, avance):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'P'
            self.valorPieza = 1
            self.avance = avance #Donde avanza, si está abajo es -1, si está arriba es 1
            self.bandera_paso = False
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
        yA, xA = origen
        yO, xO = objetivo
        if tablero.tablero[yO][xO] != ".": return False
        if "P" not in tablero.tablero[yO-1*self.avance][xO]: return False
        if self.color == BColors.WHITE and yA == yO-1*self.avance == tablero.peon_paso[0] and BColors.BLACK in tablero.tablero[yO-1*self.avance][xO]:
            self.bandera_paso = True
            return True
        if self.color == BColors.BLACK and yA == yO-1*self.avance == tablero.peon_paso[1] and BColors.WHITE in tablero.tablero[yO-1*self.avance][xO]:
            self.bandera_paso = True
            return True
        return False

    def MovimientoValido(self, tablero, origen, objetivo, necesita_camino=True):
        fila, columna = objetivo
        yA, xA = origen
        if fila <= yA and self.avance == 1: return
        if fila >= yA and self.avance == -1: return
        if abs(fila-yA) != 1 and self.contadorMovimientos > 0: return
        if abs(fila-yA) > 2 and self.contadorMovimientos == 0: return
        #ultima_Pieza_mov = tablero.registro[-1] if tablero.registro else None
        x, y = (-1, -1)
        #if ultima_Pieza_mov: y, x = ultima_Pieza_mov[2]
        if 0 <= fila < 8 and 0 <= columna < 8:  # Verifica si está dentro de los límites del tablero
            destino = tablero.tablero[fila][columna]
            if necesita_camino and self.CaminoOcupado(origen, objetivo, tablero.tablero): return False
            if abs(xA-columna) == 1 and self.EvaluarPaso(origen, objetivo, tablero): return True
            if abs(xA-columna) == 1 and destino != '.': #Va a comer a otra pieza
                if self.color == BColors.WHITE: return BColors.BLACK in destino
                if self.color == BColors.BLACK: return BColors.WHITE in destino
            if xA-columna == 0 and destino == '.': return True #Va a avanzar
        return False