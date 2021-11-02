#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 11:25:47 2021

@author: mc
"""


import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
import quantum_circuits as qcl

circuit = QuantumCircuit(4)
circuit.x(0)
# operator
circuit.barrier()
circuit.cx(0,1)
circuit.cx(0,2)
circuit.ccx(2,1,0)
circuit.ccx(0,1,3)
# inverse
circuit.barrier()
circuit.ccx(2,1,0)
circuit.cx(0,2)
circuit.cx(0,1)
circuit.measure_all()


simulator = QasmSimulator()

compiled_circuit = transpile(circuit, simulator)


job = simulator.run(compiled_circuit, shots=1000)

result = job.result()

qcl.draw_circuit(circuit)

counts = result.get_counts(compiled_circuit)

new_counts = qcl.reformat_counts(counts, 1000)
print(new_counts)