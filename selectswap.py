"""
PACKAGED: select-swap implementation of QROM

usage example: 

import selectswap

n = 3 #number of input bits
d = 5 #number of output bits

def f(x):
    #example function mapping n-bit strings to d-bit strings
    return output_bits

qrom_ckt = select_swap_qrom(n, d, f)
qrom_ckt.draw(output="mpl", style="bw")

"""

from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
from qiskit.quantum_info import Statevector, Operator
from qiskit.circuit.library import UnitaryGate
from qiskit.synthesis import OneQubitEulerDecomposer

import matplotlib.pyplot as plt

import numpy as np
import select #import the select method defined in select.py

def select_swap_qrom(n, d, f, barrier=False):
    #n: number of input qubits
    #d: number of output qubits
    #f: function mapping bitstrings of length n to bitstrings of length d

    #choose k to be ceil(n/2)
    k = (n // 2) + (n % 2)

    quantum_registerXL = QuantumRegister(n-k, name="xL")
    quantum_registerXH = QuantumRegister(k, name="xH")
    quantum_registerY = QuantumRegister(d*(2**k), name="y")
    qrom_circuit = QuantumCircuit(quantum_registerXL,quantum_registerXH, quantum_registerY, name="Select-Swap QROM")

    def fk(xL_bits):
        #returns fk defined by the function of f applied to the extended xL bits
        big_fk = ""
        for i in range(2**k):
            x_append_bits = format(i, f'0{k}b')
            x_append_bits = x_append_bits[::-1]
            x_bits = xL_bits + x_append_bits
            f_x = f(x_bits)
            big_fk += f_x
        return big_fk
    
    #select step
    sel = select_qrom(n - k, d * (2**k), fk)
    qrom_circuit.append(sel.to_gate(), quantum_registerXL[:] + quantum_registerY[:])

    #swap step
    for i in range(k)[::-1]:
        for j in range(2**i):
            for bit_index in range(d):
                ind1 = j*d + bit_index
                ind2 = (j + (2**i))*d + bit_index
                qrom_circuit.cswap(quantum_registerXH[i], quantum_registerY[ind1], quantum_registerY[ind2])
            if barrier:
                qrom_circuit.barrier() #for visualization purposes, default off for actual use

    return qrom_circuit