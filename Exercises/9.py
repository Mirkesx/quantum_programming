#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 11:35:59 2022

@author: mc
"""

import quantum_circuits as qcl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.extensions import Initialize
from qiskit.providers.aer import QasmSimulator
from qiskit.quantum_info import random_statevector
import numpy as np
import random

def randbit():
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    counts = qcl.simulate(qc, 1)
    return list(counts.keys())[0]

def create_random_bits(n):
    bits = [ randbit() for i in range(n) ]
    return bits

def create_random_bases(n):
    r = create_random_bits(n)
    bases = [ "Z" if r[i] == "0" else "X" for i in range(n) ]
    return bases

def encode_message(bits, bases):
    n = len(bits)
    message = []
    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if bits[i] == "1":
            qc.x(0)
        if bases[i] == "X":
            qc.h(0)
        qc.barrier()
        message.append(qc)
    return message
        
def decode_message(message, bases):
    n = len(message)
    bits = []
    for i in range(n):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc, 1)        
        bits.append(list(counts.keys())[0])
    return bits

def modify_message(message, bases):
    n = len(message)
    new_message = []
    for i in range(n):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        new_message.append(qc)
    return new_message


def getSampleIdx(bits):
    n = len(bits)
    idx = bits.copy()
    random.shuffle(idx)
    return idx[:int(n/2)]

def BB84(n, intercept = False):
    # Alice creates n random bits
    abits = create_random_bits(n)
    print("Alice's bits: {}".format(abits))
    
    # Alice creates n random bases
    abases = create_random_bases(n)
    print("Alice's bases: {}".format(abases))
    
    # Alice applies her bases
    message = encode_message(abits, abases)
    
    
    # Eva may intrude here
    if intercept:
        ebases = create_random_bases(n)
        print("Eve's bases: {}".format(ebases))
        message = modify_message(message, ebases)
    
    # Bob creates n random bases
    bbases = create_random_bases(n)    
    print("Bob's bases: {}".format(bbases))
    
    # Bob applies his bases
    bbits = decode_message(message, bbases)
    print("Bob's bits: {}".format(bbits))
    
    # Alice and Bob compare the bit and create the sample
    same_bases = [i for i in range(n) if abases[i] == bbases[i]]
    print("Idxs of bases that are the same: {}".format(same_bases))
    sample_idx = getSampleIdx(same_bases)
    sample_idx.sort()
    print("Sample idx are: {}".format(sample_idx))
    alice_sample = [abits[i] for i in sample_idx ]
    print("Alice's sample is: {}".format(alice_sample))
    bob_sample = [bbits[i] for i in sample_idx ]
    print("Bob's sample is: {}".format(bob_sample))
    
    if alice_sample == bob_sample:
        print("No interception!")
        remaining_idx = [i for i in same_bases if i not in sample_idx ]
        key = [ abits[i] for i in remaining_idx ]
        print("The remaining idxs are: {}".format(remaining_idx))
        print("The key is: {}".format(key))
    else:
        print("Samples mismatch! Interception!")
    
    # Alice and Bob compare the sample
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    