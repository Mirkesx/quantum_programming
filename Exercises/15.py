#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:28:46 2022

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


def constOp(n):
    qc = QuantumCircuit(n+1)
    qc.x(n)
    qcl.draw_circuit(qc)
    qc = qc.to_gate()
    qc.label = "const"
    return qc

def balancedOp(n):
    qc = QuantumCircuit(n+1)
    for i in range(n):
        qc.cx(i,n)
    qcl.draw_circuit(qc)
    qc = qc.to_gate()
    qc.label = "balanced"
    return qc

def randomBalancedOp(n):
    qc = QuantumCircuit(n+1)
    for i in range(n):
        if random.random() > 0.5:
            qc.cx(i,n)
    qcl.draw_circuit(qc)
    return qc

def Deutch(cost = True):
    n = 1
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(1, "y")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, yr, cr)
    
    qc.x(yr)
    qc.barrier()
    qc.h(xr)
    qc.h(yr)
    qc.barrier()
    
    if cost:
        gate = constOp(n)
    else:
        gate = balancedOp(n)
    
    qc = qc.compose(gate, [xr]+[yr])
    qc.barrier()
    
    qc.h(xr)
    qc.barrier()
    
    qc.measure(xr, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    qcl.print_counts(counts)


def DeutchJozsa(n, cost = True):
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(1, "y")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, yr, cr)
    
    qc.x(yr)
    qc.barrier()
    qc.h(xr)
    qc.h(yr)
    qc.barrier()
    
    if cost:
        gate = constOp(n)
    else:
        gate = randomBalancedOp(n)
    
    qc = qc.compose(gate, list(range(n+1)))
    qc.barrier()
    
    qc.h(xr)
    qc.barrier()
    
    qc.measure(xr, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    qcl.print_counts(counts)



def BVOp(s):
    n = len(s)
    qc = QuantumCircuit(n+1)
    for i in range(n):
        if s[i] == "1":
            qc.cx(i,n)
        else:
            qc.i(i)
    qcl.draw_circuit(qc)
    return qc
    

def BernsteinVazirani(s):
    n = len(s)
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(1, "y")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, yr, cr)
    
    qc.x(yr)
    qc.barrier()
    qc.h(xr)
    qc.h(yr)
    qc.barrier()
    
    gate = BVOp(s)
    
    qc = qc.compose(gate, list(range(n+1)))
    qc.barrier()
    
    qc.h(xr)
    qc.barrier()
    
    for i in range(n):
        qc.measure(i, n-i-1)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    qcl.print_counts(counts)


def SimonOp(s):
    n = len(s)
    s = s[::-1]
    idx = s.find('1')
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(n, "y")
    qc = QuantumCircuit(xr,yr)
    for i in range(n):
        qc.cx(xr[i], yr[i])
    for i in range(idx,n):
        if s[i] == "1":
            qc.cx(xr[idx], yr[i])
    qcl.draw_circuit(qc)
    return qc


def Simon(s):
    n = len(s)
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(n, "y")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(xr, yr, cr)
    
    qc.h(xr)
    qc.barrier()
    
    gate = SimonOp(s)
    
    qc = qc.compose(gate, qcl.get_qbits([xr, yr]))
    qc.barrier()
    
    qc.measure(yr,cr)    
    qc.barrier()
    
    qc.h(xr)
    qc.barrier()
    
    for i in range(n):
        qc.measure(i, i)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    #qcl.print_counts(counts)
    
    for sol in counts.keys():
        dot = 0
        for i in range(n):
            r = int(s[i]) * int(sol[i])
            dot += r
        print("{} . {} = {} mod 2". format(s, sol, dot % 2))
    


































