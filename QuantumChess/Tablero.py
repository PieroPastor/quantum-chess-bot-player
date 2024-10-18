from Piezas import *

class Tablero:
    def __init__(self):
        self.tablero = [

        ]
        self.circuito = cirq.Circuit()
        self.piezas = []
        self.InicializarPiezas()
        self.rey_blanco = None
        self.rey_negro = None

    def InicializarPiezas(self):
        # Inicializamos las piezas de ambos lados
        # Blancas
        self.piezas.append([
            Torre(BColors.WHITE, (0, 0)), Caballo(BColors.WHITE, (0, 1)), Alfil(BColors.WHITE, (0, 2)),
            Dama(BColors.WHITE, (0, 3)), Rey(BColors.WHITE, (0, 4)),
            Alfil(BColors.WHITE, (0, 5)), Caballo(BColors.WHITE, (0, 6)), Torre(BColors.WHITE, (0, 7))
        ])
        self.piezas.append([Peon(BColors.WHITE, (1, i), 1) for i in range(8)])
        self.rey_blanco = self.piezas[4]  # Guardamos referencia al rey blanco
        # Negras
        self.piezas.append([
            Torre(BColors.BLACK, (7, 0)), Caballo(BColors.BLACK, (7, 1)), Alfil(BColors.BLACK, (7, 2)),
            Dama(BColors.BLACK, (7, 3)), Rey(BColors.BLACK, (7, 4)),
            Alfil(BColors.BLACK, (7, 5)), Caballo(BColors.BLACK, (7, 6)), Torre(BColors.BLACK, (7, 7))
        ])
        self.piezas.append([Peon(BColors.BLACK, (6, i), -1) for i in range(8)])
        self.rey_negro = self.piezas[20]  # Guardamos referencia al rey negro
