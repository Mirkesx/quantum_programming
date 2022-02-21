#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 16:25:42 2022

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



def andOp(inp):
    n = len(inp)
    xr = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(xr, y, cr)
    
    for i in range(n):
        if inp[i] == "1":
            qc.x(i)
    
    qc.barrier()
    
    qc.mcx(xr,y)
    
    qc.barrier()
    
    qc.measure(y, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)



def orOp(inp):
    n = len(inp)
    xr = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(xr, y, cr)
    
    for i in range(n):
        if inp[i] == "1":
            qc.x(i)
    
    qc.barrier()
    
    qc.x(xr)
    
    qc.mcx(xr,y)
    
    qc.x(xr)
    qc.x(y)
    
    qc.barrier()
    
    qc.measure(y, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)

def xorOp(inp):
    n = len(inp)
    xr = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(xr, y, cr)
    
    for i in range(n):
        if inp[i] == "1":
            qc.x(i)
    
    qc.barrier()
    
    for i in range(n):
        qc.cx(xr[i], y)
        
    qc.barrier()
    
    qc.measure(y, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)


def ibp(inp1, inp2):
    n = len(inp1)
    x1 = QuantumRegister(n, "x1")
    x2 = QuantumRegister(n, "x2")
    anc = QuantumRegister(n, "anc")
    y = QuantumRegister(1, "y")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(x1, x2, anc, y, cr)
    
    for i in range(n):
        if inp1[i] == "1":
            qc.x(x1[i])
    for i in range(n):
        if inp2[i] == "1":
            qc.x(x2[i])
    
    qc.barrier()
    
    for i in range(n):
        qc.ccx(x1[i], x2[i], anc[i])
    
    qc.barrier()
        
    for i in range(n):
        qc.cx(anc[i], y)
        
    qc.barrier()
    
    qc.measure(y, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)


def halfAdder(inp):
    n = len(inp)
    xr = QuantumRegister(n, "x")
    y = QuantumRegister(2, "y")
    cr = ClassicalRegister(2, "cr")
    qc = QuantumCircuit(xr, y, cr)
    
    for i in range(n):
        if inp[i] == "1":
            qc.x(i)
    
    qc.barrier()
    
    qc.cx(0,2)
    qc.cx(1,2)
    qc.ccx(0,1,3)
        
    qc.barrier()
    
    qc.measure(y, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)


def fullAdder(in1, in2, inci):
    x1 = QuantumRegister(1, "x1")
    x2 = QuantumRegister(1, "x2")
    ci = QuantumRegister(1, "ci")
    y = QuantumRegister(1, "y")
    s = ClassicalRegister(1, "s")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(x1,x2,ci,y,s,c)
    
    if in1 == 1:
        qc.x(x1)
    if in2 == 1:
        qc.x(x2)
    if inci == 1:
        qc.x(ci)
    qc.barrier()
    qc.ccx(x1,x2, y)
    qc.cx(x1,x2)
    qc.ccx(x2,ci,y)
    qc.cx(x2,ci)
    qc.cx(x1,x2)    
    qc.barrier()
    qc.measure(ci, s)
    qc.measure(y, c)
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    









