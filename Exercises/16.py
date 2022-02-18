#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 16:21:05 2022

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



def entangled_pair(bits="00"):
    qc = QuantumCircuit(2)
    if bits[0] == "1":
        qc.x(0)
    if bits[1] == "1":
        qc.x(1)
    qc.h(0)
    qc.cx(0,1)
    qcl.draw_circuit(qc)
    return qc

def tpAlice():
    qc = QuantumCircuit(2, 2)
    qc.cx(0,1)
    qc.h(0)
    qc.measure(0,0)
    qc.measure(1,1)
    return qc

def tpBob():
    qc = QuantumCircuit(1, 2)
    qc.z(0).c_if(0, 1)
    qc.x(0).c_if(1, 1)
    return qc

def tp(state = None):
    if state is None:
        state = random_statevector(2)
    psi = QuantumRegister(1, "psi")
    ar = QuantumRegister(1, "ar")
    br = QuantumRegister(1, "br")
    cz = ClassicalRegister(1, "cz")
    cx = ClassicalRegister(1, "cx")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(psi, ar, br, cz, cx, cr)
    
    init = Initialize(state)
    inverse_init = init.gates_to_uncompute()
    
    
    qc = qc.compose(init, psi)
    qc.barrier()
    qc = qc.compose(entangled_pair(), list(ar) + list(br))
    qc.barrier()
    qc = qc.compose(tpAlice(), list(psi) + list(ar), list(cz) + list(cx))
    qc.barrier()
    qc = qc.compose(tpBob(), br, list(cz) + list(cx))
    qc.barrier()
    qc = qc.compose(inverse_init, br)
    
    qc.measure(br, cr)
    
    qcl.draw_circuit(qc)
    
    counts = qcl.simulate(qc)
    print(counts)
    succ = failed = 0
    for key in counts.keys():
        if key[0] == "0":
            succ += int(counts[key])
        else:
            failed += int(counts[key])
    print("Teleportation succedeed {} out of {}.".format(succ, succ+failed))


def sc(bits = "00"):
    ar = QuantumRegister(1, "ar")
    br = QuantumRegister(1, "br")
    cr = ClassicalRegister(2, "cr")
    qc = QuantumCircuit(ar, br, cr)
    
    bell_pair = entangled_pair()
    bell_pair = bell_pair.to_gate()
    bell_pair.label = "b00"
    
    disentangler = bell_pair.inverse()
    disentangler.label = "bits"
    
    qc = qc.compose(bell_pair, list(ar) + list(br))
    qc.barrier()
    if bits[0] == "1":
        qc.z(0)
    if bits[1] == "1":
        qc.x(0)
    qc.barrier()
    qc = qc.compose(disentangler, list(ar) + list(br))
    qc.barrier()
    
    qc.measure(list(br)+list(ar), cr)
    
    qcl.draw_circuit(qc)
    counts = qcl.simulate(qc)
    print(counts)



def random_bits(n):
    bits = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc, 1)
        bits.append(int(list(counts.keys())[0]))
    return bits

def random_bases(n):
    bits = random_bits(n)
    bases = ["Z", "X"]
    return [ bases[bit] for bit in bits]

def encode_message(bits, bases):
    n = len(bits)
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bits[i] == 1:
            qc.x(0)
        if bases[i] == "X":
            qc.h(0)
        message.append(qc)
    return message

def measure_message(message, bases):
    n = len(message)
    new_message = []
    for i in range(n):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        new_message.append(qc)
    return new_message


def decode_message(message, bases):
    n = len(message)
    bits = []
    for i in range(n):
        qc = message[i]
        if bases[i] == "X":
            qc.h(0)
        qc.measure(0,0)
        counts = qcl.simulate(qc, 1)
        bit = int(list(counts.keys())[0])
        bits.append(bit)
    return bits

def createSample(arr, idx):
    n = len(idx)
    random.shuffle(idx)
    return [ arr[i] for i in range(int(n/2)) ], idx[:int(n/2)]

def getSampleIdx(n):
    idx = list(range(n))
    random.shuffle(idx)
    return idx[:int(n/2)]

def bb84(n, intercept = False):
    alice_bits = random_bits(n)
    alice_bases = random_bases(n)
    print("Alice's bits: \n{}".format(alice_bits))
    print("Alice's bases: \n{}".format(alice_bases))
    message = encode_message(alice_bits, alice_bases)

    if intercept is True:
        eve_bases = random_bases(n)
        print("Eve's bases: \n{}".format(eve_bases))
        message = measure_message(message, eve_bases)
    
    bob_bases = random_bases(n)
    bob_bits = decode_message(message, bob_bases)
    print("Bob's bits: \n{}".format(bob_bits))
    print("Bob's bases: \n{}".format(bob_bases))
    
    same_idx = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    same = [alice_bases[i] for i in same_idx ]
    #print("Same \n{}".format(same))
    print("SameIdx \n{}".format(same_idx))
    alice_pre_sample = [alice_bits[i] for i in same_idx]
    bob_pre_sample = [bob_bits[i] for i in same_idx]
    print("Alice's key: \n{}".format(alice_pre_sample))
    print("Bob's key: \n{}".format(bob_pre_sample))
    
    sample, sample_idx = createSample(same, same_idx)
    sample_idx.sort()
    #print("Sample {}".format(sample))
    #sample_idx = getSampleIdx(len(sample_idx))
    print("SampleIdx {}".format(sample_idx))
    
    alice_sample = [ alice_bits[i] for i in sample_idx ]
    bob_sample = [ bob_bits[i] for i in sample_idx ]
    print("Alice's sample \n{}".format(alice_sample))
    print("Bob's sample \n{}".format(bob_sample))
    if alice_sample == bob_sample:
        key_idx = [i for i in same_idx if i not in sample_idx]
        key_idx.sort()
        print("Key idx \n{}".format(key_idx))
        key = [alice_bits[i] for i in key_idx]
        print("The key is {}".format(key))
    else:
        print("Samples mismatch. Interception!")

def get_state(s):
    n = len(s)
    i = int(s,2)
    state = [0] * 2**n
    state[i] = 1
    return np.array(state)


def Id(n):
    N = 2**n
    mat = [[0] * N] *N
    mat = np.array(mat)
    for i in range(N):
        mat[i,i] = 1
    return mat

CX = Id(2)
CX[2], CX[3] = CX[3].copy(), CX[2].copy()

H = np.array([[1,1],
              [1,-1]]) / np.sqrt(2)
I = Id(1)


X = np.array([[0,1],
              [1,0]])
Z = np.array([[1,0],
              [0,-1]])
R = np.array([[1,-1],
              [-1,-1]]) / np.sqrt(2)

A = [ Z, X, H]
B = [ Z, R, H]



def bell_pairs(n):
    arr = []
    for i in range(n):
        v11 = get_state("11")
        op = np.kron(H,I)
        pairs = np.matmul(op, v11)
        pairs = np.matmul(CX, pairs)
        arr.append(pairs)
    return arr

def v11_pairs(n):
    arr = []
    for i in range(n):
        v11 = get_state("11")
        arr.append(v11)
    return arr


def random_sequence(n):
    bits = []
    for i in range(n):
        b = random.randint(0, 2)
        bits.append(b)
    return bits

def get_matching_key(alice_bases, bob_bases):
    n = len(alice_bases)
    match_ids = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i] and alice_bases[i] != 1:
            match_ids.append(i)
    return match_ids

def projective_measurement(q, M):
    return np.matmul(q, np.matmul(M, q))

def E91(n, intercept = False):
    if not intercept:
        state = bell_pairs(n)
    else:
        state = v11_pairs(n)

    alice_bits = random_sequence(n)
    alice_bases = [ "A{}".format(i+1) for i in alice_bits ]
    print("Alice's Bases: {}".format(alice_bases))
    
    bob_bits = random_sequence(n)
    bob_bases = [ "B{}".format(i+1) for i in bob_bits ]
    print("Bob's Bases: {}".format(bob_bases))
    
    print("Compute CHSH")
    N = 0
    s = 0
    for i in range(n):
        if alice_bits[i] == 0 and bob_bits[i] == 1:
           op = np.kron(A[alice_bits[i]], B[bob_bits[i]])
           v = np.matmul(op, state[i])
           v = np.matmul(state[i], v)
           s += v
           N +=1
        
        if alice_bits[i] == 0 and bob_bits[i] == 2:
           op = np.kron(A[alice_bits[i]], B[bob_bits[i]])
           v = np.matmul(op, state[i])
           v = np.matmul(state[i], v)
           s += v
           N +=1
        
        if alice_bits[i] == 1 and bob_bits[i] == 2:
           op = np.kron(A[alice_bits[i]], B[bob_bits[i]])
           v = np.matmul(op, state[i])
           v = np.matmul(state[i], v)
           s += v
           N +=1
           
        if alice_bits[i] == 1 and bob_bits[i] == 1:
           op = np.kron(A[alice_bits[i]], B[bob_bits[i]])
           v = np.matmul(op, state[i])
           v = np.matmul(state[i], v)
           s -= v
           N +=1
           
    chsh = np.abs(s*4/N) if N > 0 else 0.0
    print("CHSH value: {}".format(chsh))
    
    if chsh > 2:
        match_key = get_matching_key(alice_bits, bob_bits)
        print("Matching ids: {}".format(match_key))
    else:
        print("CHSH is lower than 2 so it has been an interception.")





























