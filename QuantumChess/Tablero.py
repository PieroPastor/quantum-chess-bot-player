from Piezas import *

class Tablero:
    def __init__(self):
        self.tablero = []
        self.circuito = cirq.Circuit()
        self.piezas = []
        self.rey_blanco = None
        self.rey_negro = None
        self.peon_paso = [3, 4] #3 para el blanco, y 4 para el negro. Es la fila donde pueden realizar el paso
        self.InicializarPiezas()
        self.InicializarTableroFisico() #Inicializa el tablero que solo mostrará strings
        self.InicializarTableroCuantico() #Inicializa el tablero cuántico que es el circuito de Cirq

    def InicializarPiezas(self):
        # Inicializamos las piezas de ambos lados
        # Blancas
        self.piezas.append([
            Torre(BColors.BLACK, (0, 0)), Caballo(BColors.BLACK, (0, 1)), Alfil(BColors.BLACK, (0, 2)),
            Dama(BColors.BLACK, (0, 3)), Rey(BColors.BLACK, (0, 4)),
            Alfil(BColors.BLACK, (0, 5)), Caballo(BColors.BLACK, (0, 6)), Torre(BColors.BLACK, (0, 7))
        ])
        self.piezas.append([Peon(BColors.BLACK, (6, i), 1) for i in range(8)])
        self.rey_negro = self.piezas[4]  # Guardamos referencia al rey negro
        # Negras
        self.piezas.append([
            Torre(BColors.WHITE, (7, 0)), Caballo(BColors.WHITE, (7, 1)), Alfil(BColors.WHITE, (7, 2)),
            Dama(BColors.WHITE, (7, 3)), Rey(BColors.WHITE, (7, 4)),
            Alfil(BColors.WHITE, (7, 5)), Caballo(BColors.WHITE, (7, 6)), Torre(BColors.WHITE, (7, 7))
        ])
        self.piezas.append([Peon(BColors.WHITE, (1, i), -1) for i in range(8)])
        self.rey_blanco = self.piezas[20]  # Guardamos referencia al rey blanco

    def InicializarTableroFisico(self):
        raise NotImplementedError

    def InicializarTableroCuantico(self):
        raise NotImplementedError

    def MovimientoEnLista(self, pieza, origen, destino):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino
        delta_fila = fila_destino - fila_origen
        delta_col = col_destino - col_origen
        return (delta_fila, delta_col) in pieza.movimientos

