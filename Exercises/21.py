#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 18:56:13 2022

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


def random_bits(n):
    bits = []
    qc = QuantumCircuit(n)
    qc.h(list(range(n)))
    qc.measure_all(list(range(n)))
    counts = qcl.simulate(qc)
    bits = [ int(list(counts.keys())[0][i]) for i in range(n) ]
    return bits


def random_bases(n):
    bits = random_bits(n)
    return ["Z" if bits[i] == 0 else "X" for i in range(n) ]


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


def decode_message(message, bases):
    bits = []
    for i in range(len(message)):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc,1)
        bits.append(int(list(counts.keys())[0]))
    return bits


def get_same_idx(b1, b2):
    n = len(b1)
    return [ i for i in range(n) if b1[i] == b2[i]]


def sample_key(abits, bbits, idx):
    n = len(idx)
    sample_idx = list(range(n))
    random.shuffle(sample_idx)
    sample_idx = sample_idx[:int(n/2)]
    sample_idx.sort()
    print("Sample_idx {}".format(sample_idx))
    key_idx = [i for i in range(n) if i not in sample_idx]
    
    asample = [abits[i] for i in sample_idx]
    akey = [abits[i] for i in key_idx]
    
    bsample = [bbits[i] for i in sample_idx]
    bkey = [bbits[i] for i in key_idx]
    print("Asample {}".format(asample))
    print("Bsample {}".format(bsample))
    
    return asample, akey, bsample, bkey
    
    
    


def BB84(n, intercept = False):
    
    abi = random_bits(n)
    aba = random_bases(n)
    print("Abi {}".format(abi))
    print("Aba {}".format(aba))
    message = encode_message(abi, aba)
    
    
    bba = random_bases(n)
    bbi = decode_message(message, bba)
    print("Bba {}".format(bba))
    print("Bbi {}".format(bbi))


    same_idx = get_same_idx(aba, bba)
    print("Sidx {}".format(same_idx))
    print("Asame {}".format([abi[i] for i in same_idx]))
    print("Bsame {}".format([bbi[i] for i in same_idx]))
    asample, akey, bsample, bkey = sample_key(abi, bbi, same_idx)
    print("Asample {}".format(asample))
    print("Bsample {}".format(bsample))
    if asample == bsample:
        print("Key safe. Value: {} == {}".format(akey, bkey))
    else:
        print("Key intercepted. Value: {} == {}".format(akey, bkey))























