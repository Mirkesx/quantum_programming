#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 08:43:35 2022

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


def SimonOracle(s):
    n = len(s)
    s = s[::-1]
    ind = s.find("1")
    
    xr = QuantumRegister(n, "xr")
    yr = QuantumRegister(n, "yr")
    qc = QuantumCircuit(xr, yr)

    for i in range(n):
        qc.cx(xr[i],yr[i])
        
    for i in range(ind, n):
        if s[i] == "1":
            qc.cx(ind, yr[i])
    
    #qcl.draw_circuit(qc)
    return qc
    




def Simon(s):
    n = len(s)
    
    xr = QuantumRegister(n, "xr")
    yr = QuantumRegister(n, "yr")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, yr, cr)

    qc.h(xr)
    qc.barrier()
    qc = qc.compose(SimonOracle(s), list(range(2*n)))
    qc.barrier()
    qc.measure(yr, cr)
    qc.barrier()
    qc.h(xr)
    qc.measure(xr, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    
    for sol in counts.keys():
        dot = 0
        for i in range(n):
            dot += int(s[i]) * int(sol[i])
            dot = dot%2
        print("{} . {} = {} mod 2".format(s, sol, dot))



def FBI(value, n):
    
    xr = QuantumRegister(n, "xr")
    qc = QuantumCircuit(xr)
    
    for i in range(n):
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
            theta = np.pi / 2**(t)
            qc.cp(theta, j, i)
            t += 1
            
    for i in range(int(n/2)):
        qc.swap(i, n-i-1)
    
    qcl.draw_circuit(qc)
    return qc


def TestQFT(value, n):
    
    fbi = FBI(value,n).to_gate()
    fbi.label = "FBI"
    iqft = QFT(n).inverse().to_gate()
    iqft.label = "QFT^"
    
    qc = QuantumCircuit(n,n)
    
    qc.h(list(range(n)))
    qc = qc.compose(fbi)
    qc = qc.compose(iqft)
    
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


def QPE(gate, n, m = 1):
    cgate = gate.control()
    
    cont = QuantumRegister(n, "cont")
    gr = QuantumRegister(m, "gr")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(cont, gr, cr)
    
    qc.h(cont)
    qc.h(gr)
    #qc.x(gr)
    
    qc.barrier()
    
    for i in range(n):
        for j in range(2**(n-i-1)):
            qc = qc.compose(cgate, [cont[i]] + [gr[k] for k in range(m)])
    
    
    qc.barrier()
    
    iqft = QFT(n).inverse().to_gate()
    iqft.label = "QFT^"
    qc = qc.compose(iqft, cont)
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    sorted_counts = qcl.sort_counts(counts)
    qcl.print_counts(sorted_counts)
    
    val = max(counts, key=counts.get)
    value = int(val,2)
    theta = value * 2 * np.pi / 2**n
    print("Rot. {} pi".format(theta/np.pi))
    N = 2**m
    M = N * (np.sin(theta/2) ** 2)
    print("Sol. {}".format(N-M))
    return N-M



def GPO(wl):
    n = len(wl[0])
    qc = QuantumCircuit(n)
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
    
    return qc

def diffuser(n):
    sol = "0"*n
    wl = [sol]
    qc = QuantumCircuit(n)
    qc.h(list(range(n)))
    qc = qc.compose(GPO(wl))
    qc.h(list(range(n)))
    return qc

def GrO(wl):
    n = len(wl[0])
    qc = QuantumCircuit(n)
    qc = qc.compose(GPO(wl))
    qc = qc.compose(diffuser(n))
    qc = qc.to_gate()
    qc.label = "GrO"
    return qc
    









