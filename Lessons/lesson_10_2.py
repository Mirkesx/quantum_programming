#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:42:12 2021

@author: mc
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
import quantum_circuits as qcl
from qiskit.quantum_info import random_statevector

def random_state():
    psi = random_statevector(2)
    return psi

def create_bell_pair():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(1,0)
    qc = qc.to_gate()
    qc.name = "BellPair"
    return qc

def encode_message(msg):
    qc = QuantumCircuit(1)
    if msg[1] == "1":
        qc.x(0)
    if msg[0] == "1":
        qc.z(0)
    qc = qc.to_gate()
    qc.name = "Encode"
    return qc

def decode_message():
    qc = QuantumCircuit(2)
    qc.cx(1,0)
    qc.h(1)
    qc = qc.to_gate()
    qc.name = "Decode"
    return qc

def DenseCoding(msg):
    if(len(msg) != 2 or msg[0] not in "01" or msg[1] not in "01"):
        return "Messaggio non valido"
    qc = QuantumCircuit(2,2)
    qc = qc.compose(create_bell_pair(), [0,1])
    qc.barrier()
    qc = qc.compose(encode_message(msg), [0])
    qc.barrier()
    qc = qc.compose(decode_message(), [0,1])
    qc.barrier()
    qc.measure(0,0)
    qc.measure(1,1)
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    shots = 1
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    qcl.draw_circuit(qc)
    counts = result.get_counts(compiled_circuit)
    #new_counts = qcl.reformat_counts(counts, shots)
    #return new_counts
    return str(list(counts.keys())[0])