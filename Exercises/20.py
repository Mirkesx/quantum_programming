#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 18:12:32 2022

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
from fractions import Fraction


def FBI(value, n):
    xr = QuantumRegister(n, "xr")
    qc = QuantumCircuit(xr)
    
    for i in range(n):
        qc.h(i)
        theta = value * np.pi / 2**i
        qc.p(theta, xr[i])
    
    #qcl.draw_circuit(qc)
    return qc


def QFT(n):
    xr = QuantumRegister(n, "xr")
    qc = QuantumCircuit(xr)
    
    for i in range(n):
        qc.h(i)
        t = 1
        for j in range(i+1, n):
            theta = np.pi / 2**t
            qc.cp(theta, i, j)
            t += 1
    
    for i in range(int(n/2)):
        qc.swap(i, n-i-1)
        
    qcl.draw_circuit(qc)
    return qc


def TestQFT(value, n):
    
    xr = QuantumRegister(n, "xr")
    cr = ClassicalRegister(n, "cr")
    
    qc = QuantumCircuit(xr, cr)
    
    qc = qc.compose(FBI(value,n), xr)
    qc = qc.compose(QFT(n).inverse(), xr)
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)


T = lib.TGate()
S = lib.SGate()
Z = lib.ZGate()

def U(theta):
    return lib.U1Gate(theta)



def GPO(wl):
    n = len(wl[0])
    
    xr = QuantumRegister(n, "x")
    qc = QuantumCircuit(xr)
    
    for sol in wl:
        for i in range(n):
            if sol[i] == "0":
                qc.x(i)
                
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        
        
        for i in range(n):
            if sol[i] == "0":
                qc.x(i)
    
    
    qcl.draw_circuit(qc)
    return qc

def diffuser(n):
    sol = "0" * n
    wl = [sol]
    
    qc = QuantumCircuit(n)
    qc.h(list(range(n)))
    qc = qc.compose(GPO(wl))
    qc.h(list(range(n)))

    qcl.draw_circuit(qc)
    return qc


def GrO(wl):
    n = len(wl[0])
    qc = QuantumCircuit(n)
    
    qc = qc.compose(GPO(wl))
    qc = qc.compose(diffuser(n))
    qc = qc.to_gate()
    qc.label = "GrO"
    return qc
    


def Grover(wl):
    n = len(wl[0])
    
    gate = GrO(wl)
    N = 2**n
    M = int(np.round(QPE(gate, n, n) + 0.5))
    t = int((np.pi/4) * np.sqrt(N/M))    
    
    xr = QuantumRegister(n, "x")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, cr)
    
    qc.h(xr)
    
    qc.barrier()
    for it in range(t):
        qc = qc.compose(gate, xr)
        qc.barrier()
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    
    sorted_counts = qcl.sort_counts(counts)
    
    qcl.print_counts(sorted_counts)
    


def QPE(gate, n, m=1):
    cont = QuantumRegister(n, "cont")
    gr = QuantumRegister(m, "gr")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(cont, gr, cr)
    
    cgate = gate.control()
    
    qc.h(cont)
    qc.h(gr)
    #qc.x(gr)
    
    qc.barrier()
    
    for i in range(n):
        for j in range(2**(n-i-1)):
            qc = qc.compose(cgate, [cont[i]] + [gr[t] for t in range(m)])
    
    qc.barrier()
    
    iqft = QFT(n).inverse().to_gate()
    iqft.label = "QFT^"

    qc = qc.compose(iqft, cont)
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    sorted_counts = qcl.sort_counts(counts)
    #qcl.print_counts(sorted_counts)
    
    value = int(list(sorted_counts.keys())[0],2)
    theta = value *2 / 2**n
    print("Theta: {} pi".format(theta))
    theta = theta * np.pi
    N = 2**m
    M =  N * np.sin(theta/2)**2
    print("Sol. {}".format(N-M))
    return N-M





























