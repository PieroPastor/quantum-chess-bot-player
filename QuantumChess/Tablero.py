import copy

import cirq
from sympy import false

from Piezas import *
from QubitAdministrator import QubitAdministrator

class Tablero:
    def __init__(self):
        self.tablero = []
        self.circuito = cirq.Circuit()
        self.piezas = []
        self.rey_blanco = None
        self.rey_negro = None
        self.peon_paso = [3, 4] #3 para el blanco, y 4 para el negro. Es la fila donde pueden realizar el paso
        self.puntaje_blancas = 0
        self.puntaje_negras = 0
        self.InicializarPiezas()
        self.InicializarTableroFisico() #Inicializa el tablero que solo mostrará strings
        self.InicializarTableroCuantico() #Inicializa el tablero cuántico que es el circuito de Cirq

    def InicializarPiezas(self):
        # Inicializamos las piezas de ambos lados
        # Negras
        self.piezas.append(Torre(BColors.BLACK, (0, 0)))
        self.piezas.append(Caballo(BColors.BLACK, (0, 1)))
        self.piezas.append(Alfil(BColors.BLACK, (0, 2)))
        self.piezas.append(Dama(BColors.BLACK, (0, 3)))
        self.piezas.append(Rey(BColors.BLACK, (0, 4)))
        self.piezas.append(Alfil(BColors.BLACK, (0, 5)))
        self.piezas.append(Caballo(BColors.BLACK, (0, 6)))
        self.piezas.append(Torre(BColors.BLACK, (0, 7)))
        for i in range(8): self.piezas.append(Peon(BColors.BLACK, (1, i), 1))
        self.rey_negro = self.piezas[4]  # Guardamos referencia al rey negro
        # Blancas
        self.piezas.append(Torre(BColors.WHITE, (7, 0)))
        self.piezas.append(Caballo(BColors.WHITE, (7, 1)))
        self.piezas.append(Alfil(BColors.WHITE, (7, 2)))
        self.piezas.append(Dama(BColors.WHITE, (7, 3)))
        self.piezas.append(Rey(BColors.WHITE, (7, 4)))
        self.piezas.append(Alfil(BColors.WHITE, (7, 5)))
        self.piezas.append(Caballo(BColors.WHITE, (7, 6)))
        self.piezas.append(Torre(BColors.WHITE, (7, 7)))
        for i in range(8): self.piezas.append(Peon(BColors.WHITE, (6, i), -1))
        self.rey_blanco = self.piezas[20]  # Guardamos referencia al rey blanco

    def InicializarTableroFisico(self):
        for i in range(8):
            aux = []
            for j in range(8): aux.append(".")
            self.tablero.append(aux)
        self.tablero[0] = [
            f"{BColors.BLACK}R{BColors.RESET}", f"{BColors.BLACK}K{BColors.RESET}", f"{BColors.BLACK}B{BColors.RESET}",
            f"{BColors.BLACK}Q{BColors.RESET}", f"{BColors.BLACK}E{BColors.RESET}",
            f"{BColors.BLACK}B{BColors.RESET}", f"{BColors.BLACK}K{BColors.RESET}", f"{BColors.BLACK}R{BColors.RESET}"
        ]
        self.tablero[1] = [f"{BColors.BLACK}P{BColors.RESET}" for i in range(8)]
        # Negras
        self.tablero[7] = [
            f"{BColors.WHITE}R{BColors.RESET}", f"{BColors.WHITE}K{BColors.RESET}", f"{BColors.WHITE}B{BColors.RESET}",
            f"{BColors.WHITE}Q{BColors.RESET}", f"{BColors.WHITE}E{BColors.RESET}",
            f"{BColors.WHITE}B{BColors.RESET}", f"{BColors.WHITE}K{BColors.RESET}", f"{BColors.WHITE}R{BColors.RESET}"
        ]
        self.tablero[6] = [f"{BColors.WHITE}P{BColors.RESET}" for i in range(8)]

    def InicializarTableroCuantico(self):
        self.circuito.append(cirq.X(QubitAdministrator.qubits[i]) for i in range(0,16)) #Inicializa el circuito en 1 para negras
        self.circuito.append(cirq.reset(QubitAdministrator.qubits[i]) for i in range(16, 48))  # Inicializa el circuito en 0 para vacío
        self.circuito.append(cirq.X(QubitAdministrator.qubits[i]) for i in range(48, 64))  # Inicializa el circuito en 1 para blancas

    @staticmethod
    def MovimientoPermitido(pieza, origen, destino):
        # Verifica si un movimiento está permitido para la pieza
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino
        delta_fila = fila_destino - fila_origen
        delta_col = col_destino - col_origen
        return (delta_fila, delta_col) in pieza.movimientos

    def Jaque(self, rey):
        # Verificamos si alguna pieza enemiga puede atacar la posición del rey
        for pos in rey.posiciones: #Recorre las posiciones del rey
            for pieza in self.piezas: #Recorre las piezas
                if pieza.estaVivo and pieza.color != rey.color: #Si la pieza está viva y es del otro equipo analiza
                    for atq in pieza.posiciones: #Revisa las posiciones de la pieza
                        if self.MovimientoPermitido(pieza, atq, pos) and pieza.MovimientoValido(self.tablero, atq, pos): return True #Si esa pieza puede moverse hay jaque
        return False

    def Clon(self):
        #Retorna un clon de sí mismo
        return copy.deepcopy(self)

    def _GetPieza(self, simbolo, turno, y, x): #Busca el símbolo y retorna su respectiva pieza
        for i in self.piezas:
            if i.color == turno and i.simbolo == simbolo and (y, x) in i.posiciones:
                return i

    def _IntercambiarCircuitosQubits(self, qubit0, qubit1):
        for i, moment in enumerate(self.circuito):
            new_moment = []
            for op in moment:
                # Intercambiar compuertas de un solo qubit
                if op.qubits == (qubit0,):
                    new_moment.append(op.with_qubits(qubit1))  # Qubit0 -> Qubit1
                elif op.qubits == (qubit1,):
                    new_moment.append(op.with_qubits(qubit0))  # Qubit1 -> Qubit0
                # Intercambiar compuertas de múltiples qubits (por ejemplo, CISWAP)
                elif qubit0 in op.qubits or qubit1 in op.qubits:
                    new_qubits = []
                    for q in op.qubits:
                        # Intercambiar qubit0 por qubit1 y viceversa en operaciones de control
                        if q == qubit0:
                            new_qubits.append(qubit1)
                        elif q == qubit1:
                            new_qubits.append(qubit0)
                        else:
                            new_qubits.append(q)
                    new_moment.append(op.with_qubits(*new_qubits))
                else:
                    # Mantener otras operaciones intactas (si las hubiera)
                    new_moment.append(op)

            # Reemplazar el momento en el circuito original con las operaciones intercambiadas
            self.circuito[i] = cirq.Moment(new_moment)

    def _DejaEnJaque(self, p, rey, origen, destino):
        copia = copy.deepcopy(self.tablero)
        copia[origen[0]][origen[1]] = "."
        copia[destino[0]][destino[1]] = p.color+p.simbolo+BColors.RESET #Copia para simular el movimiento superficialmente
        for pos in rey.posiciones: #Recorre las posiciones del rey
            for pieza in self.piezas: #Recorre las piezas
                if pieza.estaVivo and pieza.color != rey.color: #Si la pieza está viva y es del otro equipo analiza
                    for atq in pieza.posiciones: #Revisa las posiciones de la pieza
                        if self.MovimientoPermitido(pieza, atq, pos) and pieza.MovimientoValido(copia, atq, pos): return True #Si esa pieza puede moverse hay jaque
        return False

    def _DesaparecerPieza(self, simbolo, turno, y, x):
        for pieza in self.piezas:
            if pieza.color != turno and pieza.simbolo == simbolo and pieza.estaVivo: #Significa que es a quien se le va a comer o probablemente
                if (y,x) in pieza.posiciones: #Es la pieza a la que se comerá
                    pieza.estaVivo = False #Se murió la pieza
                    pieza.posiciones = []
                    if turno == BColors.WHITE: self.puntaje_blancas += pieza.valorPieza
                    else: self.puntaje_negras += pieza.valorPieza

    def _CoronarPeon(self, ha_colapsado, origen, destino, pieza, especial=None):
        peticion = ""
        while peticion.upper() not in ["R", "K", "Q", "B"] and especial == None:
            peticion = str(input("Ingrese su coronación: ")).upper()
            if peticion not in ["R", "K", "Q", "B"]: print("Pieza no disponible")
        if especial != None: peticion = especial #Especial será cuando el string lo mande el algoritmo de entrenamiento
        if not ha_colapsado:
            self.ColapsarCasillas(pieza.posiciones)
            if not self.MovimientoPermitido(pieza, pieza.posiciones[0], destino) or pieza.CaminoOcupado(pieza.posiciones[0], destino, self.tablero): return pieza #Al final no se movio
        aux = pieza
        match peticion:
            case "R": pieza = Torre(aux.color, aux.posiciones[0])
            case "K": pieza = Caballo(aux.color, aux.posiciones[0])
            case "Q": pieza = Dama(aux.color, aux.posiciones[0])
            case "B": pieza = Alfil(aux.color, aux.posiciones[0])
        pieza.contadorMovimientos = aux.contadorMovimientos
        for i in range(32):
            if self.piezas[i] == aux: self.piezas[i] = pieza #Cambia el objeto
        return pieza

    def Split(self, origen, destinos, turno): #Division de una pieza en varios lugares
        raise NotImplementedError

    def Slide(self, origen, destino, turno): #Entrelazamiento con otros lugares
        raise NotImplementedError

    def Merge(self, origen, destino, turno): #Permite juntar dos piezas superpuestas
        raise NotImplementedError

    def Move(self, origen, destino, turno): #Movimiento basico
        yA, xA = origen
        yO, xO = destino
        if self.tablero[yA][xA] == "." or self.tablero[yA][xA][0:5] != turno: return #Turno será de tipo BColor.WHITE o BColor.BLACK
        simbolo = self.tablero[yA][xA][5]
        pieza = self._GetPieza(simbolo, turno, yA, xA)
        if not self.MovimientoPermitido(pieza, origen, destino) or pieza.CaminoOcupado(origen, destino, self.tablero): return #No es cuántico y no hay camino, por lo que no hay entrelazamiento
        if self._DejaEnJaque(pieza, self.rey_negro if pieza.color == BColors.BLACK else self.rey_blanco, origen, destino): return #No puede dejar al rey en jaque
        #Se analiza si va a comer o no
        if self.tablero[yO][xO] == ".": #En caso no coma se intercambian circuitos entre inicio y fin
            if simbolo == "P" and (yO == 0 or yO == 7): pieza = self._CoronarPeon(False, origen, destino, pieza)
            pieza.RegistrarMovimiento(tuple(origen), tuple(destino))
            #self._IntercambiarCircuitosQubits(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])) #Mueve de origen a destino
        else:
            # Si va a comer se llamará a colapso de todas las casillas involucradas con el que va a comer y el comido. Luego si se mantienen posiciones come, sino no.
            atacado = self._GetPieza(self.tablero[yO][xO][5], BColors.BLACK if turno == BColors.WHITE else BColors.WHITE, yO, xO)
            self.ColapsarCasillas(pieza.posiciones+atacado.posiciones) #Colapsará todo lo relacionado a esas casillas
            #Ahora tomará como origen el camino desde donde colapsó la pieza
            origen = pieza.posiciones[0]
            yA, xA = origen
            if not self.MovimientoPermitido(pieza, origen, destino) or pieza.CaminoOcupado(origen, destino, self.tablero): return #No se pudo mover tras el colapso
            pieza.RegistrarMovimiento(tuple(origen), tuple(destino)) #Registra el movimiento
            if self.tablero[yO][xO] != ".": #Comerá
                atacado = self.tablero[yO][xO][5]
                self._DesaparecerPieza(atacado, turno, yO, xO) #Desaparece a la pieza
            #self._IntercambiarCircuitosQubits(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO]) #Movimiento normal
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])) #Mueve de origen a destino
            if simbolo == "P" and (yO == 0 or yO == 7): pieza = self._CoronarPeon(True, origen, destino, pieza)
        self.tablero[yA][xA] = "."
        self.tablero[yO][xO] = turno + pieza.simbolo + BColors.RESET

    def ColapsarCasillas(self, casillas):
        seleccionados = [QubitAdministrator.qubits[casilla[0]*8+casilla[1]] for casilla in casillas]
        operations = [op for op in self.circuito.all_operations() if any(q in seleccionados for q in op.qubits)]
        medidor = cirq.Circuit(operations)
        seleccionados = list(medidor.all_qubits()) #Me da todos los qubits involucrados por puertas que controlan y demás
        for qubit in seleccionados:
            casilla = qubit.name.replace('q', '')  # Me da la casilla que está relacionada con el número de qubit
            medidor.append(cirq.measure(qubit, key=f"m{casilla}"))
        sim = cirq.Simulator()
        result = sim.run(medidor, repetitions=64)  # Hará 64 evaluaciones
        iterador = random.randint(0, 63)  # Elegirá una de las 64
        for qubit in seleccionados: #Verá todos los qubits involucrados
            casilla = int(qubit.name.replace('q', ''))  # Me da la casilla que está relacionada con el número de qubit
            y, x = int(casilla/8), casilla%8
            self.circuito.append(cirq.reset(qubit)) #Resetea el qubit
            medicion = getattr(result.data, f"m{casilla}")  # Obtener el valor usando getattr
            resultado = medicion[iterador] #El resultado de la medición número iter del qubit número "casilla"
            if resultado and self.tablero[y][x] != ".": #Sí está ocupada la casilla
                self.circuito.append(cirq.X(qubit))  # Le da un estado de 1 porque el resultado indica que sí está ahí
                color = self.tablero[y][x][0:5] #Consigue el color de la pieza
                simbolo = self.tablero[y][x][5] #La posición 5 de todos los strings indica el tipo de pieza
                for pieza in self.piezas:
                    if [y, x] in pieza.posiciones and pieza.color == color and pieza.simbolo == simbolo: #Es la pieza de ese color pero no peon
                        for pos in pieza.posiciones:
                            self.tablero[pos[0]][pos[1]] = "." #Limpia en el tablero de strings
                        pieza.posiciones = [[y,x]] #Setea esa posición como la suya ahora.
                        break #Ya no necesita recorrer más piezas
            else: self.tablero[y][x] = "." #Está vacío


    @staticmethod
    def _NombreDelGate(operation): 
        """Obtiene un nombre corto para la operación (por ejemplo, 'H', 'X', 'CZ')."""
        if isinstance(operation.gate, cirq.Gate):
            return str(operation.gate)
        return str(operation)  # Si no es una puerta, devuelve el nombre completo de la operación

    def ImprimirCircuito(self, plot=False):
        if not plot: print(self.circuito)
        else:
            moment_spacing = 5
            circuit = self.circuito
            qubits = list(circuit.all_qubits())

            qubit_gate_count = {}
            for operation in circuit:
                for qubit in operation.qubits:
                    if qubit not in qubit_gate_count:
                        qubit_gate_count[qubit] = 0
                    qubit_gate_count[qubit] += 1

            # Obtener la cantidad máxima de compuertas por qubit
            max_gates = max(qubit_gate_count.values()) #Para regular el máximo len
            fig, ax = plt.subplots(figsize=(max_gates+5, 64))

            # Definir las posiciones de los qubits en el eje y
            y_positions = {q: i for i, q in enumerate(qubits)}

            # Dibujar los qubits como líneas horizontales
            for qubit in qubits:
                ax.hlines(y=y_positions[qubit], xmin=0, xmax=moment_spacing * len(circuit), color='black', linewidth=2)

            # Dibujar las operaciones del circuito
            for moment_index, moment in enumerate(circuit):
                for operation in moment:
                    for qubit in operation.qubits:
                        y = y_positions[qubit]
                        # Obtener el nombre corto de la operación
                        op_text = self._NombreDelGate(operation)
                        # Ajustar el ancho de la caja según el tamaño del texto
                        text_width = len(op_text) * 0.2  # Factor para ajustar el ancho de la caja
                        ax.text(moment_index * moment_spacing + text_width / 2, y, op_text,
                                ha='center', va='center',
                                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

            # Ajustar los márgenes y la estética del gráfico
            ax.set_yticks([y_positions[q] for q in qubits])
            ax.set_yticklabels([str(q) for q in qubits])
            ax.set_xticks(range(0, moment_spacing * len(circuit), moment_spacing))
            ax.set_xticklabels([f'Moment {i}' for i in range(len(circuit))])
            ax.set_xlabel("Moments")
            ax.set_title("Circuit Diagram")

            # Establecer límites para que el gráfico no se salga del área
            ax.set_xlim(0, moment_spacing * len(circuit))
            ax.set_ylim(-0.5, len(qubits) - 0.5)

            # Ajustar los márgenes de la figura
            plt.tight_layout()

            plt.show()

    def ImprimirTablero(self):
        for fila in range(8):
            print(fila + 1, end=" ")  # Números de las filas
            for col in range(8): print(self.tablero[fila][col], end=" ")
            print()
        print("  A B C D E F G H")  # Letras de las columnas