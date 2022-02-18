#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 13:02:37 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
import numpy as np
import random


def And(s):
    n = len(s)
    
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(inp, out, cr)
    
    for i in range(n):
        if s[i] == "1":
            qc.x(inp[i])
    
    qc.barrier()
    
    qc.mcx(inp, out)
    
    qc.barrier()
    
    qc.measure(out, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
    
def Or(s):
    n = len(s)
    
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(inp, out, cr)
    
    for i in range(n):
        if s[i] == "1":
            qc.x(inp[i])
    
    qc.barrier()
    
    for i in range(n):
        qc.x(inp[i])
    
    qc.mcx(inp, out)
    
    for i in range(n):
        qc.x(inp[i])
        
    qc.x(out)
    
    qc.barrier()
    
    qc.measure(out, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
def Xor(s):
    n = len(s)
    
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(inp, out, cr)
    
    for i in range(n):
        if s[i] == "1":
            qc.x(inp[i])
    
    qc.barrier()
    
    for i in range(n):
        qc.cx(inp[i], out)
    
    qc.barrier()
    
    qc.measure(out, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
def IBP(s1,s2):
    n = len(s1)
    
    i1 = QuantumRegister(n, "s1")
    i2 = QuantumRegister(n, "s2")
    anc = QuantumRegister(n, "anc")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(i1, i2, anc, out, cr)
    
    for i in range(n):
        if s1[i] == "1":
            qc.x(i1[i])
        if s2[i] == "1":
            qc.x(i2[i])
    
    qc.barrier()
    
    for i in range(n):
        qc.ccx(i1[i], i2[i], anc[i])
    
    for i in range(n):
        qc.cx(anc[i], out)
    
    qc.barrier()
    
    qc.measure(out, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
    
def HalfAdder(s1,s2):
    s1 = s1[::-1]
    s2 = s2[::-1]
    n = len(s1)
    
    i1 = QuantumRegister(n, "n1")
    i2 = QuantumRegister(n, "n2")
    out = QuantumRegister(n+1, "out")
    cr = ClassicalRegister(n+1, "cr")
    qc = QuantumCircuit(i1, i2, out, cr)
    
    for i in range(n):
        if s1[i] == "1":
            qc.x(i1[i])
        if s2[i] == "1":
            qc.x(i2[i])
    
    qc.barrier()
    
    for i in range(n):
        qc.cx(i1[i], out[i])
        qc.cx(i2[i], out[i])
        qc.mcx([ i1[i], i2[i] ], out[i+1])
        qc.barrier()
    
    qc.barrier()
    
    qc.measure(out, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    key = list(counts.keys())[0]
    print(key)
    