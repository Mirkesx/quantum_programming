#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:12:02 2021

@author: mc
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
import quantum_circuits as qcl


def coinflip():
    circuit = QuantumCircuit(1,1)
    circuit.h(0)
    circuit.measure(0,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]


def randInt(n):
    circuit = QuantumCircuit(n,n)
    for i in range(n):
        circuit.h(i)
    for i in range(n):
        circuit.measure(i,i)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return int(list(counts.keys())[0],2)
    

def epr(b1 = 0, b2 = 0):
    circuit = QuantumCircuit(2,2)
    circuit.barrier()
    if b1 == 1:
        circuit.x(0)
    if b2 == 1:
        circuit.x(1)
    circuit.barrier()
    circuit.h(0)
    circuit.cx(0,1)
    circuit.barrier()
    circuit.measure(0,0)
    circuit.measure(1,1)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def ghz(b1, b2, b3):
    circuit = QuantumCircuit(3,3)
    circuit.barrier()
    if b1 == 1:
        circuit.x(0)
    if b2 == 1:
        circuit.x(1)
    if b3 == 1:
        circuit.x(1)
    circuit.barrier()
    circuit.h(0)
    circuit.cx(0,1)
    circuit.cx(0,2)
    circuit.barrier()
    circuit.measure(0,0)
    circuit.measure(1,1)
    circuit.measure(2,2)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

#generalized epr
def gepr(l):
    n = len(l)
    circuit = QuantumCircuit(n,n)
    circuit.barrier()
    for i in range(n):
        if l[i] == 1:
            circuit.x(i)
    circuit.barrier()
    circuit.h(0)
    for i in range(1,n):
        circuit.cx(0,i)
    circuit.barrier()
    for i in range(n):
        circuit.measure(i,i)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]
    
def swap(a, b):
    circuit = QuantumCircuit(2,2)
    circuit.barrier()
    if type(a) == list and type(b) == list:  
        circuit.initialize(a,0)
        circuit.initialize(b,1)
    elif type(a) == int and type(b) == int:
        if a == 1:
            circuit.x(0)
        if b == 1:
            circuit.x(1)
    else:
        a = 0
        b = 0
    circuit.barrier()
    circuit.cx(0,1)
    circuit.cx(1,0)
    circuit.cx(0,1)
    circuit.barrier()
    circuit.measure(0,0)
    circuit.measure(1,1)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0][::-1]
    

def andgate():
    circuit = QuantumCircuit(3)
    circuit.ccx(0,1,2)
    g = circuit.to_gate()
    g.name = "and"
    return g

def andc(b1, b2):
    inp = QuantumRegister(2)
    out = QuantumRegister(1)
    cr = ClassicalRegister(1)
    circuit = QuantumCircuit(inp,out,cr)
    circuit.barrier()
    if b1 == 1:
        circuit.x(0)
    if b2 == 1:
        circuit.x(1)
    circuit.barrier()
    circuit = circuit.compose(andgate(),[0,1,2])
    circuit.barrier()
    circuit.measure(2,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def orgate():
    circuit = QuantumCircuit(3)
    circuit.x(0)
    circuit.x(1)
    circuit.ccx(0,1,2)
    circuit.x(0)
    circuit.x(1)
    circuit.x(2)
    g = circuit.to_gate()
    g.name = "or"
    return g

def orc(b1, b2):
    circuit = QuantumCircuit(3,1)
    circuit.barrier()
    if b1 == 1:
        circuit.x(0)
    if b2 == 1:
        circuit.x(1)
    circuit.barrier()
    
    #sol 1
    #circuit.cx(0,2)
    #circuit.cx(1,2)
    #circuit.ccx(0,1,2)
   
    #sol 2
    #circuit.x(0)
    #circuit.x(1)
    #circuit.ccx(0,1,2)
    #circuit.x(0)
    #circuit.x(1)
    #circuit.x(2)
    circuit = circuit.compose(orgate(),[0,1,2])
   
    circuit.barrier()
    circuit.measure(2,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def xorgate():
    circuit = QuantumCircuit(3)
    circuit.cx(0,2)
    circuit.cx(1,2)
    g = circuit.to_gate()
    g.name = "xor"
    return g


def xorc(b1, b2):
    circuit = QuantumCircuit(3,1)
    circuit.barrier()
    if b1 == 1:
        circuit.x(0)
    if b2 == 1:
        circuit.x(1)
    circuit.barrier()
    
    circuit = circuit.compose(xorgate(),[0,1,2])
   
    circuit.barrier()
    circuit.measure(2,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def gandgate(blist):
    n = len(blist)
    circuit = QuantumCircuit(n)
    circuit.mcx(blist, n) # second is the target position
    g = circuit.to_gate()
    g.name = "generalized_and"
    return g

def gand(blist):
    n = len(blist)
    inp = QuantumRegister(n, "input")
    out = QuantumRegister(1, "output")
    cr = ClassicalRegister(1, "cr")
    circuit = QuantumCircuit(inp, out, cr)
    circuit.barrier()
    for i in range(n):
        if blist[i] == 1:
            circuit.x(i)
    circuit.barrier()
    
    circuit = circuit.compose(gandgate(list(range(n))),list(range(n)))
   
    circuit.barrier()
    circuit.measure(n,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def gor(blist):
    n = len(blist)
    inp = QuantumRegister(n, "input")
    out = QuantumRegister(1, "output")
    cr = ClassicalRegister(1, "cr")
    circuit = QuantumCircuit(inp, out, cr)
    circuit.barrier()
    for i in range(n):
        if blist[i] == 1:
            circuit.x(i)
    
    for i in range(n):
        circuit.x(i)
    circuit.barrier()
    
    circuit.mcx(list(range(n)), n)
    
    for i in range(n+1):
        circuit.x(i)
    circuit.barrier()
    circuit.measure(n,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

def gxorgate(n):
    circuit = QuantumCircuit(n+1)
    for i in range(n):
        circuit.cx(i,n)
    g = circuit.to_gate()
    g.name = "generalized_xor"
    return g

def gxorc(blist):
    n = len(blist)
    inp = QuantumRegister(n, "input")
    out = QuantumRegister(1, "output")
    cr = ClassicalRegister(1, "cr")
    circuit = QuantumCircuit(inp, out, cr)
    circuit.barrier()
    for i in range(n):
        if blist[i] == 1:
            circuit.x(i)
    circuit.barrier()
    
    #for i in range(n):
    #    circuit.cx(i,n)
    circuit = circuit.compose(gxorgate(n), list(range(n+1)))
   
    circuit.barrier()
    circuit.measure(n,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]


#inner product
def dotp(x, y):
    if len(x) != len(y):
        return -1
    n = len(x)
    
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(n, "y")
    anc = QuantumRegister(n, "ancilla_bit")
    out = QuantumRegister(1, "out")
    cr = ClassicalRegister(1, "cr")
    circuit = QuantumCircuit(xr, yr, anc, out, cr)
    circuit.barrier()
    
    for i in range(n):
        if int(x[i]) == 1:
            circuit.x(xr[i])
        if int(y[i]) == 1:
            circuit.x(yr[i])
            
    circuit.barrier()
    
    for i in range(n):
        #circuit.ccx(xr[i], yr[i], anc[i])
        circuit = circuit.compose(andgate(),[xr[i],yr[i],anc[i]])
        #circuit = circuit.compose(andgate(), [i, i+n, i+2*n])
    
    circuit.barrier()
    
    circuit = circuit.compose(gxorgate(n), list(range(2*n, 3*n+1))) #[anc])
    #for i in range(n):
    #    circuit.cx(anc[i],out)
    
    circuit.barrier()
    circuit.measure(out,0)
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    #qcl.draw_circuit()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

























