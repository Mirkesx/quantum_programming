#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 18:02:48 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
import numpy as np
import random


def bvGate(s):
    n = len(s)
    q1 = QuantumRegister(n)
    q2 = QuantumRegister(1)
    qc = QuantumCircuit(q1,q2)
    
    for i in range(n):
        if s[i] == '1':
            qc.cx(q1[i],q2)
    
    qc = qc.to_gate()
    qc.label = "Uf"
    return qc
    


def BV(s):
    n = len(s)
    inp = QuantumRegister(n, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(inp, out, cr)
    
    qc.x(out)
    
    qc.barrier()
    
    qc.h(inp)
    qc.h(out)
    
    qc.barrier()
    
    qc = qc.compose(bvGate(s), list(inp) + list(out))
    
    qc.barrier()
    
    qc.h(inp)
    
    qc.barrier()
    
    qc.measure(inp, cr[::-1])
    qcl.draw_circuit(qc)
    
    counts = simulate(qc)
    print(counts)



def simulate(qc):
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    shots = 1000
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    #qcl.draw_circuit(qc)
    counts = result.get_counts(compiled_circuit)
    #new_counts = qcl.reformat_counts(counts, shots)
    #return new_counts
    return counts
    return int(list(counts.keys())[0])    