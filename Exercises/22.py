#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 15:34:51 2022

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


def random_bit():
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    
    counts = qcl.simulate(qc, 1)
    return int(list(counts.keys())[0])


def random_sequence(n):
    return [ random_bit() for i in range(n) ]


def random_bases(n):
    bits = random_sequence(n)
    return [ "Z" if bits[i] == 0 else "X" for i in range(n) ]


def encode_message(bits, bases):
    message = []
    for i in range(len(bits)):
        qc = QuantumCircuit(1,1)
        if bits[i] == 1:
            qc.x(0)
        if bases[i] == "X":
            qc.h(0)
        message.append(qc)
    return message

def measure_message(message, bases):
    new_message = []
    for i in range(len(message)):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        new_message.append( qc )
    return new_message



def decode_message(message, bases):
    bits = []
    for i in range(len(message)):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc, 1)
        bits.append( int(list(counts.keys())[0]) )
    return bits

def get_sample_key_idx(idxs):
    arr = idxs.copy()
    n = len(arr)
    random.shuffle(arr)
    sample_idx = arr[:int(n/2)]
    key_idx = arr[int(n/2):]
    sample_idx.sort()
    key_idx.sort()
    return key_idx, sample_idx


def BB84(n, intercept = False):
    
    abi = random_sequence(n)
    abb = random_bases(n)
    print("Abi {}".format(abi))
    print("Abb {}".format(abb))
    message = encode_message(abi, abb)
    
    
    if intercept:
        ebb = random_bases(n)
        message = measure_message(message, ebb)
    
    
    
    bbb = random_bases(n)
    bbi = decode_message(message, bbb)
    print("Bbb {}".format(bbb))
    print("Bbi {}".format(bbi))
    
    match_idx = [ i for i in range(n) if abb[i] == bbb[i] ]
    key_idx, sample_idx = get_sample_key_idx(match_idx)
    print("Key_idx: {}".format(key_idx))
    print("Sample_idx: {}".format(sample_idx))
    
    asa = [abi[i] for i in sample_idx]
    bsa = [bbi[i] for i in sample_idx]
    print("Asa: {}".format(asa))
    print("Bsa: {}".format(bsa))
    if len(sample_idx) > 0 and asa == bsa:
        print("Key safe.")
        key = [abi[i] for i in key_idx]
        print("Key {}".format(key))
    else:
        print("Key intercepted!")
    
    
    return 



































