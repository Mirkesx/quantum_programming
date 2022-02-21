#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 12:25:13 2022

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



def encode_message(bits, bases):
    message = []
    for i in range(len(bits)):
        qc = QuantumCircuit(1,1)
        if bits[i] == 1:
            qc.x(0)
        if bases[i] == 1:
            qc.h(0)
        message.append(qc)
    return message


def interception(message, bases):
    new_message = []
    for i in range(len(bases)):
        qc = message[i]
        if bases[i] == 1:
            qc.h(0)
        qc.measure(0,0)
        new_message.append(qc)
    return new_message


def decode_message(message, bases):
    bits = []
    for i in range(len(bases)):
        qc = message[i]
        if bases[i] == 1:
            qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc,1)
        bit = int(list(counts.keys())[0])
        bits.append(bit)
    return np.array(bits)


def BB84(n, intercept = False):
    
    alice_bits = np.random.randint(0,2,n,int)
    alice_bases = np.random.randint(0,2,n,int)
    print("Abi: {}".format(alice_bits))
    print("Aba: {}".format(alice_bases))
    message = encode_message(alice_bits, alice_bases)
    
    if intercept:
        eve_bases = np.random.randint(0,2,n,int)
        print("Eba: {}".format(eve_bases))
        message = interception(message, eve_bases)
        
    bob_bases = np.random.randint(0,2,n,int)
    bob_bits = decode_message(message, bob_bases)
    print("Bba: {}".format(bob_bases))
    print("Bbi: {}".format(bob_bits))
    
    
    matching_idx = np.array([ i for i in range(n) if alice_bases[i] == bob_bases[i] ])
    print("Match idx: {}".format(matching_idx))
    n_match = len(matching_idx)
    random_idx = list(range(n_match))
    random.shuffle(random_idx)
    sample_idx = [matching_idx[random_idx[i]] for i in range(int(n_match/2)) ]
    sample_idx.sort()
    key_idx = [i for i in matching_idx if i not in sample_idx]
    print("Sample idx: {}".format(sample_idx))
    print("Key idx: {}".format(key_idx))
    
    alice_sample = [alice_bits[i] for i in sample_idx]
    bob_sample = [bob_bits[i] for i in sample_idx]
    print("Asa: {}".format(alice_sample))
    print("Bsa: {}".format(bob_sample))
    if alice_sample == bob_sample:
        print("Key safe!")
        print("Key: {}".format([alice_bits[i] for i in key_idx]))
    else:
        print("Key not safe!")
    
    
    return





















































