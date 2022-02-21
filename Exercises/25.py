#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 12:10:25 2022

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



def halfAdder(x1, x2):
    xr = QuantumRegister(2, "xr")
    yr = QuantumRegister(2, "yr")
    s = ClassicalRegister(1, "sum")
    c = ClassicalRegister(1, "carry")
    qc = QuantumCircuit(xr, yr, s, c)
    
    if x1 == 1:
        qc.x(xr[0])
        
    if x2 == 1:
        qc.x(xr[1])

    qc.barrier()
    
    qc.cx(0,2)
    qc.cx(1,2)
    qc.ccx(0,1,3)
    
    
    qc.barrier()
    
    qc.measure(yr[0], s)
    qc.measure(yr[1], c)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc,1)
    print(counts)


def fullAdder(x1, x2, c0):
    xr = QuantumRegister(2, "xr")
    yr = QuantumRegister(2, "yr")
    s = ClassicalRegister(1, "sum")
    c = ClassicalRegister(1, "carry")
    qc = QuantumCircuit(xr, yr, s, c)
    
    if x1 == 1:
        qc.x(xr[0])
        
    if x2 == 1:
        qc.x(xr[1])
        
    if c0 == 1:
        qc.x(yr[0])

    qc.barrier()
    
    qc.ccx(0,1,3)
    qc.cx(0,1)
    qc.ccx(1,2,3)
    qc.cx(1,2)
    qc.cx(0,1)
    
    
    qc.barrier()
    
    qc.measure(yr[0], s)
    qc.measure(yr[1], c)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc,1)
    print(counts)





























