#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 18:27:33 2022

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


def halfAdder(inp):
    qc = QuantumCircuit(4,2)
    
    if inp[2] == "1":
        qc.x(1)
    if inp[0] == "1":
        qc.x(0)
        
    qc.barrier()
    qc.cx(0,2)
    qc.cx(1,2)
    qc.mcx([0,1],3)
    qc.barrier()
    
    qc.measure(3,0)
    qc.measure(2,1)
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)
    

def fullAdder(inp):
    qc = QuantumCircuit(4,2)
    
    if inp[2] == "1":
        qc.x(1)
    if inp[0] == "1":
        qc.x(0)
    if inp[4] == "1":
        qc.x(2)
        
    qc.barrier()
    qc.mcx([0,1],3)
    qc.cx(0,1)
    qc.mcx([1,2],3)
    qc.cx(1,2)
    qc.cx(0,1)
    qc.barrier()
    
    qc.measure(3,1)
    qc.measure(2,0)
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)
    

def cO(n=1):
    qc = QuantumCircuit(n+1)
    qc.x(n)
    return qc

def bO(n=1):
    qc = QuantumCircuit(n+1)
    qc.cx(0,n)
    return qc

def DeutchJozsa(n, gate):
    qc = QuantumCircuit(n+1,n)
    
    qc.x(n)
    qc.barrier()
    qc.h(list(range(n+1)))
    qc.barrier()
    qc = qc.compose(gate, list(range(n+1)))
    qc.barrier()
    
    qc.h(list(range(n)))
    qc.barrier()
    
    qc.measure(list(range(n)), list(range(n)))
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)
    

def bvO(s):
    n = len(s)
    qc = QuantumCircuit(n+1)
    for i in range(n):
        if s[i] == "1":
            qc.cx(i, n)
    return qc

def BernsteinVazirani(s):
    n = len(s)
    qc = QuantumCircuit(n+1,n)
    
    qc.x(n)
    qc.barrier()
    qc.h(list(range(n+1)))
    qc.barrier()
    qc = qc.compose(bvO(s), list(range(n+1)))
    qc.barrier()
    
    qc.h(list(range(n)))
    qc.barrier()
    
    for i in range(n):
        qc.measure(i, n-i-1)
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)

def sO(s):
    n = len(s)
    s = s[::-1]
    ind = s.find("1")
    qc = QuantumCircuit(2*n)
    
    for i in range(n):
        qc.cx(i, i+n)
    
    for i in range(ind, n):
        if s[i] == '1':
            qc.cx(ind, i+n)
        
    qcl.draw_circuit(qc)
    return qc
    
    
def Simon(s):
    n = len(s)
    
    inp = QuantumRegister(n)
    out = QuantumRegister(n)
    cr = ClassicalRegister(n)
    
    qc = QuantumCircuit(inp, out, cr)
    
    qc.h(inp)
    qc.barrier()

    qc = qc.compose(sO(s), qcl.get_qbits([inp, out]))
    
    qc.barrier()
    qc.measure(out, cr)
    
    qc.barrier()
    qc.h(inp)
    qc.barrier()
    qc.measure(inp, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    
    for sol in counts.keys():
        dot = 0
        for i in range(n):
            dot += int(sol[i]) * int(s[i])
        dot = dot % 2
        print("{} . {} = {} mod 2".format(s, sol, dot))
    























