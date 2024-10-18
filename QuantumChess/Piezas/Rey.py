from Pieza import *

class Rey(Pieza):
    def __init__(self, color, pos):
        if color == BColors.WHITE or color == BColors.BLACK:
            super().__init__(color, pos)
            self.simbolo = 'E'
            self.valorPieza = sys.maxsize
            self.CargaMovimiento()
        else: raise NotImplementedError

    def CargaMovimiento(self):
        self.movimientos.append((1, 1))  # diagonal derecha abajo
        self.movimientos.append((-1, 1))  # diagonal izquierda abajo
        self.movimientos.append((1, -1))  # diagonal derecha arriba
        self.movimientos.append((-1, -1))  # diagonal izquierda arriba
        self.movimientos.append((1, 0))  # avanza a la derecha de A a H
        self.movimientos.append((-1, 0))  # Avanza a la izquierda de H a A
        self.movimientos.append((0, 1))  # avanza a la abajo de A a H
        self.movimientos.append((0, -1))  # Avanza a la arriba de H a A
        self.movimientos.append((0, 2))  # enroque corto
        self.movimientos.append((0, -2))  # enroque largo

    def RegistrarMovimiento(self, origen, objetivo):
        super().RegistrarMovimiento(objetivo)
        if self.contadorMovimientos == 1:
            self.movimientos.remove((0, 2))
            self.movimientos.remove((0, -2))

    def EvaluarEnroque(self, tablero, objetivo):
        fila, columna = objetivo
        yA, xA = self.posicionReal
        global bandera_de_enroque
        for mov in self.movimientos:
            yM, xM = mov
            if (yA + yM, xM + xA) == objetivo:
                if columna == 2:
                    pieza = tablero.tablero[fila][0]  # escoje la torre [1,2,3]
                    if pieza.color == self.color and pieza.simbolo == 'R' and pieza.contadormovimientos == 0 and \
                            tablero.tablero[fila][1] is None and tablero.tablero[fila][2] is None and \
                            tablero.tablero[fila][3] is None:
                        bandera_de_enroque = True
                        return True
                elif columna == 6:
                    pieza = tablero.tablero[fila][7]  # escoje la torre [5  6]
                    if pieza.color == self.color and pieza.simbolo == 'R' and pieza.contadormovimientos == 0 and \
                            tablero.tablero[fila][5] is None and tablero.tablero[fila][6] is None:
                        bandera_de_enroque = True
                        return True
        bandera_de_enroque = False
        return False

    def MovimientoValido(self, tablero, origen, objetivo):
        y, x = objetivo
        if (x == 2 or x == 6) and (y == 0 or y == 7): return self.EvaluarEnroque(tablero, objetivo)
        else: return super().MovimientoValido(tablero, objetivo)