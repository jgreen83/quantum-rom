"""
PACKAGED: select implementation of QROM

usage example: 

import select

n = 3 #number of input bits
d = 5 #number of output bits

def f(x):
    #example function mapping n-bit strings to d-bit strings
    return output_bits

qrom_ckt = select_qrom(n, d, f)
qrom_ckt.draw(output="mpl", style="bw")

"""


from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
from qiskit.quantum_info import Statevector, Operator
from qiskit.circuit.library import UnitaryGate
from qiskit.synthesis import OneQubitEulerDecomposer

import matplotlib.pyplot as plt

import numpy as np

def select_qrom(n, d, f):
    #n: number of input qubits
    #d: number of output qubits
    #f: function mapping bitstrings of length n to bitstrings of length d

    quantum_registerX = QuantumRegister(n, name="x")
    quantum_registerY = QuantumRegister(d, name="y")
    qrom_circuit = QuantumCircuit(quantum_registerX, quantum_registerY, name="Select")

    for i in range(2**n):
        x_bits = format(i, f'0{n}b')  
        f_x = f(x_bits)    
        if '1' in f_x:
            for i in range(n):
                if( x_bits[i] == '0'):
                    qrom_circuit.x(quantum_registerX[i])

            for j in range(d):
                if f_x[j] == '1':
                    qrom_circuit.mcx([quantum_registerX[k] for k in range(n)], quantum_registerY[j])
            for i in range(n):
                if( x_bits[i] == '0'):
                    qrom_circuit.x(quantum_registerX[i])
                

    return qrom_circuit
