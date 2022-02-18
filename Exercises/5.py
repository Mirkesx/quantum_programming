#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 19:00:35 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
import numpy as np
import random

def Or(s):
    inp = QuantumRegister(2)
    anc = QuantumRegister(1)
    out = QuantumRegister(1)
    final_res = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(inp, out, anc, final_res, cr)
    
    if s[0] == "1":
        qc.x(inp[0])
    if s[1] == "1":
        qc.x(inp[1])
        
    qc.barrier()
    
    qc.ccx(inp[0], inp[1],anc)
    qc.cx(anc, out)
    qc.cx(out, final_res)
    qc.cx(anc, out)
    qc.ccx(inp[0], inp[1],anc)
    
    qc.barrier()
    qc.measure_all()
    
    qcl.draw_circuit(qc)
    
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    shots = 1000
    job = simulator.run(compiled_circuit, shots)
    results = job.result()
    counts = results.get_counts(compiled_circuit)
    return counts

    
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
    