from Utils import *

class QubitAdministrator:
    qubits = [cirq.NamedQubit(f"q{i}") for i in range(64)]
