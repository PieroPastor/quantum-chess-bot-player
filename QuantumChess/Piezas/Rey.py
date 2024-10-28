from .Pieza import *

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
        super().RegistrarMovimiento(origen, objetivo)
        if self.contadorMovimientos == 1:
            self.movimientos.remove((0, 2))
            self.movimientos.remove((0, -2))

    def EvaluarEnroque(self, objetivo, tablero, piezas):
        fila, columna = objetivo
        if self.color == BColors.BLACK and piezas[4].contadorMovimientos > 0: return False #Analiza al rey
        if self.color == BColors.WHITE and piezas[20].contadorMovimientos > 0: return False
        global bandera_de_enroque
        if columna == 2:
            torre = tablero[fila][0] #Selecciona la torre
            if torre == 'R' and piezas[(self.color == BColors.WHITE)*16+(self.color == BColors.BLACK)*0].contadorMovimientos == 0 and \
                tablero[fila][1] == '.' and tablero[fila][2] == '.' and tablero[fila][3] == '.':
                bandera_de_enroque = True
                return True
        elif columna == 6:
            torre = tablero[fila][7]  # Selecciona la torre
            if torre == 'R' and piezas[(self.color == BColors.WHITE)*23+(self.color == BColors.BLACK)*7].contadorMovimientos == 0 and \
                tablero[fila][5] == '.' and tablero[fila][6] == '.':
                bandera_de_enroque = True
                return True
        bandera_de_enroque = False
        return False

    def MovimientoValido(self, tablero, origen, objetivo, necesita_camino=True):
        y, x = objetivo
        if (x == 2 or x == 6) and (y == 0 or y == 7): return self.EvaluarEnroque(objetivo, tablero.tablero, tablero.piezas)
        else: return super().MovimientoValido(tablero, origen, objetivo, necesita_camino)