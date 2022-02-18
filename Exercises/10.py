#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:15:43 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import random_statevector
import numpy as np
import random

def Cgate(n = 1):
    qc = QuantumCircuit(n + 1)
    gate = qc.to_gate()
    gate.label = "Constant Gate"
    return gate    

def Ggate(n = 1):
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i,n)
    gate = qc.to_gate()
    gate.label = "General Gate"
    return gate    



def Deutch(gate = Cgate()):
    inp = QuantumRegister(1, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    
    qc = QuantumCircuit(inp, out, cr)
    
    # a0
    qc.barrier()
    qc.x(out)
    
    # a1
    qc.barrier()
    qc.h(inp)
    qc.h(out)
    
    # a2
    qc.barrier()
    qc.append(gate, qcl.get_qbits([inp, out]))
    
    # a3
    qc.barrier()
    qc.h(inp)
    
    # a4
    qc.barrier()
    qc.measure(inp, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
    
    
def DeutchJozsa(n, gate = None):
    if gate is None:
        gate = Cgate(n)
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(n, "cr")
    
    qc = QuantumCircuit(inp, out, cr)
    
    # a0
    qc.barrier()
    qc.x(out)
    
    # a1
    qc.barrier()
    qc.h(inp)
    qc.h(out)
    
    # a2
    qc.barrier()
    qc.append(gate, qcl.get_qbits([inp, out]))
    
    # a3
    qc.barrier()
    qc.h(inp)
    
    # a4
    qc.barrier()
    qc.measure(inp, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
    
    
def BVOracle(s):
    n = len(s)
    qc = QuantumCircuit(n+1)
    for i in range(n):
        if s[i] == "0":
            qc.i(i)
        else:
            qc.cx(i,n)
    return qc
    gate = qc.to_gate()
    gate.label = "BV Gate"
    return gate    
    
def BV(s):
    n = len(s)
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(n, "cr")
    
    qc = QuantumCircuit(inp, out, cr)
    
    # a0
    qc.barrier()
    qc.x(out)
    
    # a1
    qc.barrier()
    qc.h(inp)
    qc.h(out)
    
    # a2
    qc.barrier()
    qc = qc.compose(BVOracle(s), qcl.get_qbits([inp, out]))
    
    # a3
    qc.barrier()
    qc.h(inp)
    
    # a4
    qc.barrier()
    qc.measure(inp, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)
   
    
def SimonOracle(s):
    n = len(s)
    rev_s = s[::-1]
    idx_first_one = rev_s.index("1")
    qc = QuantumCircuit(2*n)
    for i in range(n):
        qc.cx(i,n+i)
    for i in range(idx_first_one, n):
        if rev_s[i] == "1":
            qc.cx(idx_first_one, n+i)
    return qc
    gate = qc.to_gate()
    gate.label = "Simon Gate"
    return gate   
    
def test_result(a,b):
    s = 0
    for i in range(len(a)):
        s += int(a[i])*int(b[i])
        s = s%2
    return s
    
def Simon(s):
    n = len(s)
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(n, "out")
    cr = ClassicalRegister(n, "cr")
    
    qc = QuantumCircuit(inp, out, cr)
    
    # a0
    qc.barrier()
    
    # a1
    qc.barrier()
    qc.h(inp)
    
    # a2
    qc.barrier()
    qc = qc.compose(SimonOracle(s), qcl.get_qbits([inp, out]))
    
    # a3
    qc.barrier()
    qc.measure(out, cr)
    qc.h(inp)
    
    # a4
    qc.barrier()
    qc.measure(inp, cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    keys = list(counts.keys())
    for i in range(len(keys)):
        res = test_result(keys[i], s)
        if res == 0:
            print("{} . {} = 0 mod 2".format(keys[i], s))
        else:
            print("{} is not orthogonal with {}".format(keys[i], s))