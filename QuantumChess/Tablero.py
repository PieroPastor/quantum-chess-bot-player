from Utils import *

from Piezas import *
from QubitAdministrator import QubitAdministrator

class Tablero:
    def __init__(self):
        self.tablero = []
        self.probabilidades = []
        self.circuito = cirq.Circuit()
        self.piezas = []
        self.rey_blanco = None
        self.rey_negro = None
        self.peon_paso = [3, 4] #3 para el blanco, y 4 para el negro. Es la fila donde pueden realizar el paso
        self.puntaje_blancas = 0
        self.puntaje_negras = 0
        self.InicializarPiezas()
        self.InicializarTableroFisico() #Inicializa el tablero que solo mostrará strings
        self.InicializarTableroProbabilidades() #Inicializa el tablero que solo tendrá la probabilidad por pieza
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

    def InicializarTableroProbabilidades(self):
        for i in range(8):
            aux = []
            if i == 0 or i == 1 or i == 6 or i == 7:
                for j in range(8): aux.append(float(100))
            else:
                for j in range(8): aux.append(float(0))
            self.probabilidades.append(aux)

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

    @staticmethod
    def MismaFilaMovimientos(origen, destino1, destino2):
        fila_origen, col_origen = origen
        fila_destino1, col_destino1 = destino1
        fila_destino2, col_destino2 = destino2
        y1, y2 = (fila_destino1 - fila_origen), (fila_destino2 - fila_origen)
        x1, x2 = (col_destino1 - col_origen), (col_destino2 - col_origen)
        if x1 == 0 and x2 == 0:
            if y1 >= 0 and y2 >= 0: return True
            if y1 < 0 and y2 < 0: return True
        if y1 == 0 and y2 == 0:
            if x1 >= 0 and x2 >= 0: return True
            if x1 < 0 and x2 < 0: return True
        if x1 != 0 and x2 != 0:
            m1, m2 = float(y1 / x1), float(y2 / x2)
            if m1 == m2:  # Misma pendiente = misma direccion
                if y1 >= 0 and y2 >= 0 and x1 >= 0 and x2 >= 0: return True
                if y1 < 0 and y2 < 0 and x1 < 0 and x2 < 0: return True
                if y1 >= 0 and y2 >= 0 and x1 < 0 and x2 < 0: return True
                if y1 < 0 and y2 < 0 and x1 >= 0 and x2 >= 0: return True
        return False

    def GetRey(self, color):
        if color == 'B': return self.piezas[4]
        elif color == 'W': return self.piezas[20]

    def Jaque(self, rey):
        # Verificamos si alguna pieza enemiga puede atacar la posición del rey
        for pos in rey.posiciones: #Recorre las posiciones del rey
            for pieza in self.piezas: #Recorre las piezas
                if pieza.estaVivo and pieza.color != rey.color: #Si la pieza está viva y es del otro equipo analiza
                    for atq in pieza.posiciones: #Revisa las posiciones de la pieza
                        if self.MovimientoPermitido(pieza, atq, pos) and pieza.MovimientoValido(self.tablero, atq, pos): return True #Si esa pieza puede moverse hay jaque
        return False
        
    def JaqueMate(self,rey):
        if not self.Jaque(rey):
            return False
        for mov in rey.movimientos:
            ym,xm=mov
            for pos in rey.posiciones:
                yp,xp=pos
                if not self._DejaEnJaque(rey,rey,pos,(ym+yp,xm+xp)):
                    return False
        return True
    
    def JaqueAhogado(self,rey):
        if self.Jaque(rey):
            return False
        for mov in rey.movimientos:
            ym,xm=mov
            for pos in rey.posiciones:
                yp,xp=pos
                if not self._DejaEnJaque(rey,rey,pos,(ym+yp,xm+xp)):
                    return False
        return True       
        
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
        if 0 > destino[0] or destino[0] >= 8: return False
        copia = copy.deepcopy(self.tablero)
        copia[origen[0]][origen[1]] = "."
        copia[destino[0]][destino[1]] = p.color+p.simbolo+BColors.RESET #Copia para simular el movimiento superficialmente
        es_rey = False
        if p.simbolo == "E":
            es_rey = True
            rey.posiciones.append(tuple(destino))
            rey.posiciones.remove(tuple(origen))
        for pos in rey.posiciones: #Recorre las posiciones del rey
            for pieza in self.piezas: #Recorre las piezas
                if pieza.estaVivo and pieza.color != rey.color: #Si la pieza está viva y es del otro equipo analiza
                    for atq in pieza.posiciones: #Revisa las posiciones de la pieza
                        if self.MovimientoPermitido(pieza, atq, pos) and pieza.MovimientoValido(copia, atq, pos):
                            if es_rey:
                                rey.posiciones.remove(tuple(destino))
                                rey.posiciones.append(tuple(origen))
                            return True #Si esa pieza puede moverse hay jaque
        if es_rey:
            rey.posiciones.remove(tuple(destino))
            rey.posiciones.append(tuple(origen))
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
            entrelazadas = []
            piezas = [pieza]
            for p in piezas:
                for e in p.entrelazadas:
                    if self.piezas[e] not in piezas:
                        piezas.append(self.piezas[e])
                        entrelazadas += self.piezas[e].historial
            self.ColapsarCasillas(pieza.historial+entrelazadas)
            if not self.MovimientoPermitido(pieza, pieza.posiciones[0], destino) or not pieza.MovimientoValido(self, pieza.posiciones, destino): return pieza #Al final no se movio
        aux = pieza
        match peticion:
            case "R": pieza = Torre(aux.color, aux.posiciones[0])
            case "K": pieza = Caballo(aux.color, aux.posiciones[0])
            case "Q": pieza = Dama(aux.color, aux.posiciones[0])
            case "B": pieza = Alfil(aux.color, aux.posiciones[0])
        pieza.contadorMovimientos = aux.contadorMovimientos
        pieza.historial = deepcopy(aux.historial)
        for i in range(32):
            if self.piezas[i] == aux: self.piezas[i] = pieza #Cambia el objeto
        return pieza

    def Split(self, origen, destino1, destino2, turno, coronacion=None): #Division de una pieza en varios lugares
        yA, xA = origen
        yO1, xO1 = destino1
        yO2, xO2 = destino2
        d1, d2 = math.sqrt((yA-yO1)**2+(xA-xO1)**2), math.sqrt((yA-yO2)**2+(xA-xO2)**2)
        if d2 > d1: #Para así analizar primero la distancia más lejana
            aux = destino2
            destino2 = destino1
            destino1 = aux
            yO1, xO1 = destino1
            yO2, xO2 = destino2
        if yA < 0 or yA >= 8 or xA < 0 or xA >= 8: return
        if self.tablero[yA][xA] == "." or self.tablero[yA][xA][0:5] != turno: return  # Turno será de tipo BColor.WHITE o BColor.BLACK
        #Analiza si hay posibilidad de comer
        if (self.tablero[yO1][xO1][0:5] == BColors.BLACK and turno == BColors.WHITE) or \
                (self.tablero[yO1][xO1][0:5] == BColors.WHITE and turno == BColors.BLACK): self.Move(origen, destino1, turno, coronacion)
        elif (self.tablero[yO2][xO2][0:5] == BColors.BLACK and turno == BColors.WHITE) or \
                (self.tablero[yO2][xO2][0:5] == BColors.WHITE and turno == BColors.BLACK): self.Move(origen, destino2, turno, coronacion)
        simbolo = self.tablero[yA][xA][5]
        #En caso haya posibilidad de coronación
        if simbolo == "P" and (yO1 == 0 or yO1 == 7): self.Move(origen, destino1, turno, coronacion)
        if simbolo == "P" and (yO2 == 0 or yO2 == 7): self.Move(origen, destino2, turno, coronacion)
        pieza = self._GetPieza(simbolo, turno, yA, xA)
        if not self.MovimientoPermitido(pieza, origen, destino1) or not self.MovimientoPermitido(pieza, origen, destino2): return
        if self._DejaEnJaque(pieza, self.rey_negro if pieza.color == BColors.BLACK else self.rey_blanco, origen, destino1) \
                or self._DejaEnJaque(pieza, self.rey_negro if pieza.color == BColors.BLACK else self.rey_blanco, origen, destino2): return  # No puede dejar al rey en jaque
        hay_slide1 = False
        hay_slide2 = False
        misma_direccion = self.MismaFilaMovimientos(origen, destino1, destino2) #Indica que no hay relacion entre los splits
        if not pieza.MovimientoValido(self, origen, destino1):
            if not pieza.MovimientoValido(self, origen, destino1, necesita_camino=False): return  # Si falla aquí fue error no de bloqueo
            if not pieza.MovimientoValido(self, origen, destino2, necesita_camino=False): return # Para no hacer nada si fallaría aquí
            se_movio = self.Slide(origen, destino1, turno)  # Manda a analizar si puede hacer un slide
            if not se_movio: return  # No es cuántico y no hay camino, por lo que no hay entrelazamiento
            hay_slide1 = True
        if not pieza.MovimientoValido(self, origen, destino2):
            if not pieza.MovimientoValido(self, origen, destino2, necesita_camino=False): return  # Si falla aquí fue error no de bloqueo
            se_movio = True
            if not hay_slide1:
                se_movio = self.Slide(origen, destino2, turno) #Si no hubo slide antes, este será el primero
                hay_slide2 = True
            elif misma_direccion:
                self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yO1*8+xO1], QubitAdministrator.qubits[yO2*8+xO2])**0.5) #Si ya hubo un slide antes, este es el segundo
                self.probabilidades[yO2][yO2] = self.probabilidades[xO1][xO1] / 2
                self.probabilidades[xO1][xO1] /= 2
                self.tablero[yO2][xO2] = pieza.color+pieza.simbolo+BColors.RESET
                pieza.RegistrarMovimiento((yO2, xO2), (yO2, xO2))
                hay_slide2 = True
            elif hay_slide1:
                se_movio = self.Slide(origen, destino2, turno, 0.5) #Si no hubo slide antes, este será el primero
                hay_slide2 = True
            if not se_movio: return  # No es cuántico y no hay camino, por lo que no hay entrelazamiento

        if (not hay_slide1 and hay_slide2) or (not hay_slide2 and hay_slide1):
            if hay_slide1 and not hay_slide2:
                self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO2*8+xO2])**0.5)
                self.probabilidades[yO2][xO2] = self.probabilidades[yO1][xO1]/2
                self.probabilidades[yO1][xO1] /= 2
                pieza.RegistrarMovimiento((yO2, xO2), (yO2, xO2))
            elif not hay_slide1 and hay_slide2:
                self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO1*8+xO1])**0.5)
                self.probabilidades[yO1][yO1] = self.probabilidades[xO2][xO2]/2
                self.probabilidades[xO2][xO2] /= 2
                pieza.RegistrarMovimiento((yO1, xO1), (yO1, xO1))
            self.tablero[yO1][xO1] = self.tablero[yO2][xO2] = self.tablero[yA][xA]
        elif not hay_slide1 and not hay_slide2:
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO1*8+xO1])**0.5)
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO2*8+xO2]))
            self.probabilidades[yO1][xO1] = self.probabilidades[yO2][xO2] = self.probabilidades[yA][xA]/2
            self.probabilidades[yA][xA] = 0
            self.tablero[yO1][xO1] = self.tablero[yO2][xO2] = self.tablero[yA][xA]
            self.tablero[yA][xA] = "."
            pieza.RegistrarMovimiento((yA, xA), (yO1, xO1))
            pieza.RegistrarMovimiento((yA, xA), (yO2, xO2))

    #Checker se encargará de si es true solo de simulación, para saber si se puede mover
    def Slide(self, origen, objetivo, turno, potencia=1.0, checker=False): #Entrelazamiento con otros lugares
        yO, xO = objetivo
        yA, xA = origen
        simbolo = self.tablero[yA][xA][5]
        pieza = self._GetPieza(simbolo, turno, yA, xA)
        this_pieza = self.piezas.index(pieza)
        entrelazados_casillas = []
        entrelazados_indices = []
        if 0 <= yO < 8 and 0 <= xO < 8:  # Verifica si está dentro de los límites del tablero
            destino = self.tablero[yO][xO]
            if destino != '.':
                if turno == BColors.WHITE and BColors.BLACK not in destino: return False
                if turno == BColors.BLACK and BColors.WHITE not in destino: return False
            if yA - yO == 0:
                aux = abs(xA - xO)
                for i in range(1, aux):
                    if self.tablero[yA][xA + ((xO < xA) * -1) * 2 * i + i] != '.':
                        p = self.tablero[yA][xA + ((xO < xA) * -1) * 2 * i + i][5]
                        objeto = self._GetPieza(p, self.tablero[yA][xA + ((xO < xA) * -1) * 2 * i + i][0:5], yA, xA + ((xO < xA) * -1) * 2 * i + i)
                        indice = self.piezas.index(objeto)
                        casilla = yA*8+(xA + ((xO < xA) * -1) * 2 * i + i)
                        if len(objeto.posiciones) == 1: return False
                        else:
                            if indice not in entrelazados_indices: entrelazados_indices.append(indice)
                            if casilla not in entrelazados_casillas: entrelazados_casillas.append(casilla)
            elif xA - xO == 0:
                aux = abs(yA - yO)
                for i in range(1, aux):
                    if self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA] != '.':
                        p = self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA][5]
                        objeto = self._GetPieza(p, self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA][0:5], yA + ((yO < yA) * -1) * 2 * i + i, xA)
                        indice = self.piezas.index(objeto)
                        casilla = (yA + ((yO < yA) * -1) * 2 * i + i) * 8 + xA
                        if len(objeto.posiciones) == 1: return False
                        else:
                            if indice not in entrelazados_indices: entrelazados_indices.append(indice)
                            if casilla not in entrelazados_casillas: entrelazados_casillas.append(casilla)
            else:
                distancia = int(math.sqrt((yA - yO) ** 2 + (xA - xO) ** 2))
                for i in range(1, distancia):
                    if self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA + ((xO < xA) * -1) * 2 * i + i] != '.':
                        p = self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA + ((xO < xA) * -1) * 2 * i + i][5]
                        objeto = self._GetPieza(p, self.tablero[yA + ((yO < yA) * -1) * 2 * i + i][xA + ((xO < xA) * -1) * 2 * i + i][0:5], yA + ((yO < yA) * -1) * 2 * i + i, xA + ((xO < xA) * -1) * 2 * i + i)
                        indice = self.piezas.index(objeto)
                        casilla = (yA + ((yO < yA) * -1) * 2 * i + i) * 8 + (xA + ((xO < xA) * -1) * 2 * i + i)
                        if len(objeto.posiciones) == 1: return False
                        else:
                            if indice not in entrelazados_indices: entrelazados_indices.append(indice)
                            if casilla not in entrelazados_casillas: entrelazados_casillas.append(casilla)
            if checker: return True #Si solo era análisis, entonces retorna True porque llegó hasta aquí
            pieza.entrelazadas += entrelazados_indices
            for i in entrelazados_indices: self.piezas[i].entrelazadas.append(this_pieza)
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO]).controlled_by(*[QubitAdministrator.qubits[i] for i in entrelazados_casillas], control_values=[0 for _ in entrelazados_casillas])**potencia)
            self.tablero[yO][xO] = pieza.color+pieza.simbolo+BColors.RESET
            pieza.RegistrarMovimiento((yO, xO), (yO, xO))
            self.probabilidades[yO][xO] = self.probabilidades[yA][xA] / 2
            self.probabilidades[yA][xA] /= 2
            return True
        return False

    def Merge(self, origen1, origen2, destino, turno, coronacion=None): #Permite juntar dos piezas superpuestas
        #self.circuito.append(QubitAdministrator.merge_gate.on(#qubits))
        raise NotImplementedError

    def Move(self, origen, destino, turno, coronacion=None): #Movimiento basico
        yA, xA = origen
        yO, xO = destino
        if yA < 0 or yA >= 8 or xA < 0 or xA >= 8: return
        if self.tablero[yA][xA] == "." or self.tablero[yA][xA][0:5] != turno: return #Turno será de tipo BColor.WHITE o BColor.BLACK
        simbolo = self.tablero[yA][xA][5]
        pieza = self._GetPieza(simbolo, turno, yA, xA)
        if self._DejaEnJaque(pieza, self.rey_negro if pieza.color == BColors.BLACK else self.rey_blanco, origen, destino): return  # No puede dejar al rey en jaque
        if not self.MovimientoPermitido(pieza, origen, destino): return
        if not pieza.MovimientoValido(self, origen, destino):
            if not pieza.MovimientoValido(self, origen, destino, necesita_camino=False): return #Si falla aquí fue error no de bloqueo
            if self.tablero[yO][xO] != ".": return
            se_movio = self.Slide(origen, destino, turno) #Manda a analizar si puede hacer un slide
            return
        yAtq = yO
        #Se analiza si va a comer o no
        bandera_de_comer_al_paso = False
        if isinstance(pieza, Peon):
            bandera_de_comer_al_paso = pieza.bandera_paso
            pieza.bandera_paso = False
        if self.tablero[yO][xO] == "." and not bandera_de_comer_al_paso: #En caso no coma se intercambian circuitos entre inicio y fin
            if simbolo == "P" and (yO == 0 or yO == 7): pieza = self._CoronarPeon(False, origen, destino, pieza, coronacion)
            pieza.RegistrarMovimiento(tuple(origen), tuple(destino))
            #self._IntercambiarCircuitosQubits(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])) #Mueve de origen a destino
            self.probabilidades[yO][xO] = self.probabilidades[yA][xA]
            self.probabilidades[yA][xA] = 0
        else:
            # Si va a comer se llamará a colapso de todas las casillas involucradas con el que va a comer y el comido. Luego si se mantienen posiciones come, sino no.
            if isinstance(pieza, Peon): yAtq = yO-1*bandera_de_comer_al_paso*pieza.avance
            atacado = self._GetPieza(self.tablero[yAtq][xO][5], BColors.BLACK if turno == BColors.WHITE else BColors.WHITE, yAtq, xO)
            entrelazadas = []
            piezas = [pieza, atacado]
            for p in piezas:
                for e in p.entrelazadas:
                    if self.piezas[e] not in piezas:
                        piezas.append(self.piezas[e])
                        entrelazadas += self.piezas[e].historial
            self.ColapsarCasillas(pieza.historial+atacado.historial+entrelazadas) #Colapsará todo lo relacionado a esas casillas
            #Ahora tomará como origen el camino desde donde colapsó la pieza
            if self.tablero[yA][xA] == ".": return
            origen = pieza.posiciones[0]
            yA, xA = origen
            if not self.MovimientoPermitido(pieza, origen, destino) or not pieza.MovimientoValido(self, origen, destino): return #No se pudo mover tras el colapso
            pieza.RegistrarMovimiento(tuple(origen), tuple(destino)) #Registra el movimiento
            if self.tablero[yAtq][xO] != ".": #Comerá
                atacado = self.tablero[yAtq][xO][5]
                self._DesaparecerPieza(atacado, turno, yAtq, xO) #Desaparece a la pieza
            #self._IntercambiarCircuitosQubits(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO]) #Movimiento normal
            self.circuito.append(cirq.ISWAP(QubitAdministrator.qubits[yA*8+xA], QubitAdministrator.qubits[yO*8+xO])) #Mueve de origen a destino
            self.probabilidades[yO][xO] = self.probabilidades[yA][xA]
            self.probabilidades[yA][xA] = 0
            if simbolo == "P" and (yO == 0 or yO == 7): pieza = self._CoronarPeon(True, origen, destino, pieza, coronacion)
        self.tablero[yA][xA] = self.tablero[yAtq][xO] = "."
        self.tablero[yO][xO] = turno + pieza.simbolo + BColors.RESET

    def GetMoves(self, color):
        if color == 'W': color = '\033[97m'
        else: color = '\033[30m'
        moves = []
        turno = color
        for pieza in self.piezas:
            if pieza.color == color:
                for origen in pieza.posiciones:
                    yA, xA = origen
                    posibles_prev = [] #Guardará todos los movimientos posibles parciales
                    for mov in pieza.movimientos:
                        destino = (origen[0]+mov[0], origen[1]+mov[1])
                        if 0 <= destino[0] < 8 and 0 <= destino[1] < 8:
                            yO, xO = destino
                            if self.tablero[yA][xA] == "." or self.tablero[yA][xA][0:5] != turno: continue  # Turno será de tipo BColor.WHITE o BColor.BLACK
                            if self._DejaEnJaque(pieza,self.rey_negro if pieza.color == BColors.BLACK else self.rey_blanco, origen, destino): continue
                            if not pieza.MovimientoValido(self, origen, destino):
                                if self.tablero[yO][xO] != ".": continue
                                if not pieza.MovimientoValido(self, origen, destino, necesita_camino=False): continue  # Si falla aquí fue error no de bloqueo
                                se_movio = self.Slide(origen, destino, turno, checker=True)  # Manda a analizar si puede hacer un slide
                                if se_movio:
                                    moves.append((1, origen, 0, destino, 0, 0, color))
                                    posibles_prev.append((destino, 0))
                                continue #Ya sea si se mueve o no, ya no es necesario analizar el resto
                            # No importa si come o no, si llegó hasta aquí es importante de analizar
                            if pieza.simbolo == "P" and (yO == 0 or yO == 7):
                                for i in range(1,5):
                                    moves.append((1, origen, 0, destino, 0, i, color)) #Manda a coronar para cada pieza
                                    posibles_prev.append((destino, i))
                                continue
                            moves.append((1, origen, 0, destino, 0, 0, color)) #Así coma o no, igual se mueve y es lo que importa
                            posibles_prev.append((destino, 0))
                    for mov in posibles_prev: #Recorre todos los destinos posibles para armar combinaciones en split
                        for mov2 in posibles_prev:
                            if mov == mov2: continue
                            coronacion = max(mov[1], mov2[1]) #Cualquiera que tenga coronacion la toma
                            moves.append((2, origen, 0, mov[0], mov2[0], coronacion, color)) #Bota split y toma los dos destinos
        return moves

    def GenericMove(self, move):
        kinda = move[0]
        from1 = move[1]
        from2 = move[2]
        to1 = move[3]
        to2 = move[4]
        crown = move[5]
        turn = move[6]
        match crown:
            case 0: crown = None
            case 1: crown = "R"
            case 2: crown = "Q"
            case 3: crown = "B"
            case 4: crown = "K"
        match kinda:
            case 1: self.Move(from1, to1, turn, crown)
            case 2: self.Split(from1, to1, to2, turn, crown)
            case 3: self.Merge(from1, from2, to1, turn, crown)

    def ColapsarCasillas(self, casillas):
        seleccionados = [QubitAdministrator.qubits[casilla[0]*8+casilla[1]] for casilla in casillas]
        '''
        while True: #Consigue el circuito histórico de todos los qubits
            operations = [op for op in self.circuito.all_operations() if any(q in seleccionados for q in op.qubits)]
            medidor = cirq.Circuit(operations)
            seleccionados2 = list(medidor.all_qubits()) #Me da todos los qubits involucrados por puertas que controlan y demás
            if seleccionados2 == seleccionados: break
            seleccionados = seleccionados2
        seleccionados = seleccionados2
        '''
        operations = [op for op in self.circuito.all_operations() if any(q in seleccionados for q in op.qubits)]
        medidor = cirq.Circuit(operations)
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
                    if (y, x) in pieza.posiciones and pieza.color == color and pieza.simbolo == simbolo: #Es la pieza de ese color pero no peon
                        for pos in pieza.posiciones:
                            self.tablero[pos[0]][pos[1]] = "." #Limpia en el tablero de strings
                            self.probabilidades[pos[0]][pos[1]] = 0
                        pieza.posiciones = [(y,x)] #Setea esa posición como la suya ahora.
                        pieza.historial = [(y,x)]
                        pieza.entrelazadas = [] #Ya no está entrelazado a nada
                        self.probabilidades[y][x] = 100
                        self.tablero[y][x] = pieza.color+pieza.simbolo+BColors.RESET
                        break #Ya no necesita recorrer más piezas
            else:
                self.tablero[y][x] = "." #Está vacío
                self.probabilidades[y][x] = 0


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

    def ImprimirProbabilidades(self):
        for fila in range(8):
            print(fila + 1, end=" ")  # Números de las filas
            for col in range(8): print(self.probabilidades[fila][col], end=" ")
            print()
        print("  A B C D E F G H")  # Letras de las columnas
