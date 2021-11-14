#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 12:04:54 2021

@author: mc
"""


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import random_statevector
import quantum_circuits as qcl
import random


def simulate(qc):
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    shots = 1
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    #qcl.draw_circuit(qc)
    counts = result.get_counts(compiled_circuit)
    #new_counts = qcl.reformat_counts(counts, shots)
    #return new_counts
    return int(list(counts.keys())[0])



def randbit():
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    return simulate(qc)



def random_sequence(n):
    return [randbit() for i in range(n)]



def random_bases(n):
    b = []
    s = random_sequence(n)
    for i in range(n):
        if s[i] == 1:
            b.append('Z')
        else:
            b.append('X')
    return b



def encode_message(bits, bases):
    message = []
    for i in range(len(bits)):
        qc = QuantumCircuit(1,1)
        if(bits[i] == 1):
            qc.x(0)
        if(bases[i] == "X"):
            qc.h(0)
        qc.barrier()
        message.append(qc)
    return message



def measure_message(message, bases):
    n = len(message)
    for i in range(n):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.barrier()
        qc.measure(0,0)
        message[i] = qc
    return message



def decode_message(message, bases):
    bits = []
    message = measure_message(message, bases)
    for i in range(len(message)):
        qc = message[i]
        bits.append(simulate(qc))
    return bits



def getSampleIdx(n):
    idx = list(range(n))
    random.shuffle(idx)
    return idx[:int(n/2)]



def BB84(n, intercept = False):
    # Alice sceglie n bits casualmente
    alice_bits = random_sequence(n)
    print("Alice's Bits")
    print(alice_bits)
    # Alice genera le n basi casualmente
    alice_bases = random_bases(n)
    print("Alice's Bases")
    print(alice_bases)
    # Alice crea il messaggio
    message = encode_message(alice_bits, alice_bases)
    # Alice manda il messaggio a Bob
    
    if intercept:
        # Eve sceglie le n basi casualmente
        #eve_bases = random_bases(n)
        eve_bases = ["Z"] * n
        print("Eve's Bases")
        print(eve_bases)
        message = measure_message(message, eve_bases)
    
    # Bob sceglie le n basi casualmente
    bob_bases = random_bases(n)
    print("Bob's Bases")
    print(bob_bases)
    # Bob misura gli n bit dopo aver applicato le n basi
    bob_bits = decode_message(message, bob_bases)
    print("Bob's Bits")
    print(bob_bits)
    # Alice e Bob si scambiano le basi e le confrontono
    match = [ i for i in range(n) if bob_bases[i] == alice_bases[i] ]
    # Alice e Bob creano le loro chiavi segrete
    alice_key = [ alice_bits[i] for i in match ]
    bob_key = [ bob_bits[i] for i in match ]
    print("Alice's key:")
    print(alice_key)
    print("Bob's key:")
    print(bob_key)
    # Alice e Bob creano un sample e verificano che sia corretto
    sample_idx = getSampleIdx(len(bob_key))
    alice_sample = [ alice_key[i] for i in sample_idx ]
    bob_sample = [ bob_key[i] for i in sample_idx ]
    print("Alice's sample")
    print(alice_sample)
    print("Bob's sample")
    print(bob_sample)
    if alice_sample == bob_sample:
        # Nessuna intercettazione
        print("Valid Key")
        alice_key = [ alice_key[i] for i in range(len(sample_idx)) if i not in sample_idx ]
        bob_key = [ bob_key[i] for i in range(len(sample_idx)) if i not in sample_idx ]
        
        if alice_key == bob_key:
            print(bob_key)
            print("Key len: {}".format(len(alice_key)))
        else:
            print("Error")
    else:
        # Intercettato
        print("Message intercepted. Key is not safe.")
            
    



















