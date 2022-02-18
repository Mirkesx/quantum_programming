#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 11:45:02 2022

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



def FBI(value, n):
    xr = QuantumRegister(n)
    qc = QuantumCircuit(xr)
    qc.h(xr)
    for i in range(n):
        theta = value * np.pi / 2**(i)
        qc.p(theta, xr[i])
    #qcl.draw_circuit(qc)
    return qc

def QFT(n):
    xr = QuantumRegister(n)
    qc = QuantumCircuit(xr)
    for i in range(n):
        qc.h(xr[i])
        t = 1
        for j in range(i+1, n):
            theta =  np.pi / 2**t
            qc.cp(theta, i, j)
            t += 1
    
    for i in range(int(n/2)):
        qc.swap(i, n-i-1)       
    #qcl.draw_circuit(qc)
    return qc
    

def TestQFT(value, n):
    xr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(xr, cr)
    
    fbi = FBI(value,n)
    iqft = QFT(n).inverse()
    iqft = iqft.to_gate()
    iqft.label = "IQFT^"
    
    qc = qc.compose(fbi,xr)
    qc = qc.compose(iqft,xr)
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    qcl.print_counts(counts)
    
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
    
    #qcl.draw_circuit(qc)
    return qc

def diffuser(n):
    xr = QuantumRegister(n, "x")
    qc = QuantumCircuit(xr)
    sol = "0"*n
    gpo = GPO([sol])
    qc.h(xr)
    qc = qc.compose(gpo)    
    qc.h(xr)
    #qcl.draw_circuit(qc)
    return qc


def GrO(wl):
    n = len(wl[0])
    xr = QuantumRegister(n, "x")
    qc = QuantumCircuit(xr)
    gpo = GPO(wl)
    diff = diffuser(n)
    qc = qc.compose(gpo)  
    qc = qc.compose(diff)    
    #qcl.draw_circuit(qc)
    qc = qc.to_gate()
    qc.label = "GrO"
    return qc
    

    
def QPE(gate, n, m=1):
    cgate = gate.control()
    xr = QuantumRegister(n, "cont")
    gr = QuantumRegister(m, "aux")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, gr, cr)
    qc.h(xr)
    qc.h(gr)
    #qc.x(gr)
    for i in range(n):
        for j in range(2**(n-i-1)):
            qc = qc.compose(cgate, [xr[i]] + [ gr[t] for t in range(m)])
        qc.barrier()
    
    iqft = QFT(n).inverse()
    iqft = iqft.to_gate()
    iqft.label = "IQFT^"
    qc = qc.compose(iqft,xr)    
    
    for i in range(n):
        qc.measure(i, n-i-1)
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    sorted_counts = qcl.sort_counts(counts)
    #qcl.print_counts(sorted_counts)
    
    max_value = list(sorted_counts.keys())[0]
    max_value = int(max_value,2)
    theta = max_value * 2 * np.pi / 2**n
    print("Rotazione: {} pi".format(theta/np.pi))
    N = 2**m
    M = int(N - N * (np.sin(theta/2)**2))
    print("Soluzioni: {}".format(M))
    return M


def Grover(wl):
    n = len(wl[0])
    N = 2**n
    gate = GrO(wl)
    M = QPE(gate, n, n)
    xr = QuantumRegister(n, "x")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, cr)
    qc.h(xr)
    t = int(np.floor( (np.pi / 4 ) * np.sqrt(N/M) ))
    for it in range(t):
        qc = qc.compose(gate, xr)
    for i in range(n):
        qc.measure(i, n-i-1)
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    sorted_counts = qcl.sort_counts(counts)
    qcl.print_counts(sorted_counts)
































