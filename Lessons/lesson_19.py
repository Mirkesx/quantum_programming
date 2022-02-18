#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 18:45:11 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import random_statevector
import numpy as np
import random


def FBI(value, n):
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
        phase = (np.pi/2**q) * value
        qc.p(phase, q)
    #qcl.draw_circuit(qc)
    return qc


def QFT(n):
    qc = QuantumCircuit(n)
    
    for t in range(n):
        qc.h(t)
        i = 1
        for c in range(t+1, n):
            phase = np.pi/(2**i)
            qc.cp(phase, c, t)
            i = i*2
        
    for q in range(int(n/2)):
        qc.swap(q, n-q-1)
    
    #qcl.draw_circuit(qc)
    return qc


def TestQFT(value, n):
    qc = QuantumCircuit(n, n)
    qc = qc.compose(FBI(value, n))
    iqft = QFT(n).inverse()
    #iqft = iqft.to_gate()
    #iqft.label = "QFT^"
    
    qc = qc.compose(iqft)
    
    
    for q in range(n):
        qc.measure(q, n-q-1)
        
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)