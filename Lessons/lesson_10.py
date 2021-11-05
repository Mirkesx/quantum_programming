#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:42:12 2021

@author: mc
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import random_statevector
import quantum_circuits as qcl

def random_state():
    psi = random_statevector(2)
    return psi

def create_bell_pair():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    return qc

def alice_gate():
    psi = QuantumRegister(1, "message")
    ar = QuantumRegister(1, "alice qbit")
    cr = ClassicalRegister(2, "code")
    qc = QuantumCircuit(psi, ar, cr)
    
    qc.cx(psi, ar)
    qc.h(psi)
    qc.barrier()
    
    
    qc.measure(psi,cr[0])
    qc.measure(ar,cr[1])
    
    return qc

def bob_gate():
    qubit = QuantumRegister(1, "bob qbit")
    crz = ClassicalRegister(1, "crz")
    crx = ClassicalRegister(1, "crx")
    qc = QuantumCircuit(qubit, crz, crx)
    
    # classical if, controlla se i due valori combaciano
    qc.x(qubit).c_if(crx,1)
    qc.z(qubit).c_if(crz,1)
    
    return qc


def Teleportation(psi):
    qr = QuantumRegister(1, "message")
    ar = QuantumRegister(1, "alice qbit")
    br = QuantumRegister(1, "bob qbit")
    crz = ClassicalRegister(1, "crz")
    crx = ClassicalRegister(1, "crx")
    vr = ClassicalRegister(1, "verify")
    qc = QuantumCircuit(qr, ar, br, crz, crx, vr)

    init_gate = Initialize(psi)
    init_gate.label = "init"
    inverse_init_gate = init_gate.gates_to_uncompute()

    qc = qc.compose(init_gate, qcl.get_qbits([qr]))
    qc.barrier()
    qc = qc.compose(create_bell_pair(), qcl.get_qbits([ar, br]))
    qc.barrier()
    qc = qc.compose(alice_gate(), qcl.get_qbits([qr, ar]), qcl.get_qbits([crz, crx]))
    qc.barrier()
    qc = qc.compose(bob_gate(), qcl.get_qbits([br]), qcl.get_qbits([crz, crx]))
    #qc = qc.compose(inverse_init_gate, qcl.get_qbits([qr]))
    qc.append(inverse_init_gate, qcl.get_qbits([br]))
    qc.measure(br, vr)
    qcl.draw_circuit(qc)
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    shots = 1000
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    count0 = 0
    count1 = 0
    for key in counts.keys():
        if key[0] == "0":
            count0 += counts[key]
        else:
            count1 += counts[key]
    print("Times the message was correctly received: {} \nTimes the message was not correctly received: {}".format(count0, count1))
    new_counts = qcl.reformat_counts(counts, shots)
    return new_counts

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
    qc = qc.compose(encode_message(msg), [1])
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




