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
import qiskit.circuit.library as lib
import numpy as np
import random


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

T = lib.TGate()
S = lib.SGate()
Z = lib.ZGate()

def U(theta):
    return lib.U1Gate(theta)


def Test(theta):
    qc = QuantumCircuit(1,1)
    qc.x(0)
    qc = qc.compose(U(theta))
    qc.measure(0,0)
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)


def QPE(gate, n, m=1):
    
    pr = QuantumRegister(n, "phase")
    gr = QuantumRegister(m, "gr")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(pr, gr, cr)
    
    qc.h(pr)
    qc.x(gr)
    qc.barrier()
    cgate = gate.control()
    
    for i in range(n):
        for r in range(2**(n-i-1)):
            qc = qc.compose(cgate, [pr[i], gr[0]])
    
    
    qc.barrier()
    iqft = QFT(n).inverse()
    iqft = iqft.to_gate()
    iqft.label = "QFT^"
    
    qc.append(iqft, pr)
    
    for q in range(n):
        qc.measure(q, n-q-1)
        
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)
    
    counts = list(counts)
    counts.sort(reverse=True)
    theta = counts[0]
    val = int(theta, 2)
    val = 2*val/2**n
    print("Rotation : {} pi".format(val))