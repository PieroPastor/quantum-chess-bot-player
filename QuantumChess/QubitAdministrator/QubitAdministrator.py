import math
import sys
import cirq
import copy
import random
import matplotlib.pyplot as plt
import numpy as np

class QubitAdministrator:
    qubits = [cirq.NamedQubit(f"q{i}") for i in range(64)]
    matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, -1j, 0, 0, 0],
                       [0, -1j / np.sqrt(2), 1 / np.sqrt(2), 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, -1 / np.sqrt(2), -1j / np.sqrt(2), 0],
                       [0, -1j / np.sqrt(2), -1 / np.sqrt(2), 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1 / np.sqrt(2), -1j / np.sqrt(2), 0],
                       [0, 0, 0, -1j, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1]])

    # Define una compuerta usando la matriz
    merge_gate = cirq.MatrixGate(matrix)
