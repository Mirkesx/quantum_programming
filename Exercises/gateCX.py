#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:38:49 2021

@author: mc
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
import quantum_circuits as qcl


def cx(b1,b2):
    inp = QuantumRegister(1, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(inp, out, cr)
    qc.barrier()
    if b1 == 1:
        qc.x(inp)
    if b2 == 1:
        qc.x(out)
    qc.barrier()
    qc.cx(inp, out)
    qc.measure(out, cr)
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    qcl.draw_circuit(qc)
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]


def simcx(b1,b2):
    inp = QuantumRegister(1, "inp")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(inp, out, cr)
    qc.barrier()
    if b1 == 1:
        qc.h(inp)
        qc.z(inp)
        qc.h(inp)
    if b2 == 1:
        qc.h(out)
        qc.z(out)
        qc.h(out)
    qc.barrier()
    qc.h(out)
    qc.cz(inp,out)
    qc.h(out)
    qc.measure(out, cr)
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    qcl.draw_circuit(qc)
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]
