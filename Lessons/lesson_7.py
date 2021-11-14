# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

def get_state(bin_str):
    if type(bin_str) == str:
        n = len(bin_str)
        N = 2**n
        state = [0] * N
        pos = int(bin_str, 2)
        state[pos] = 1
        return np.array(state)
    elif type(bin_str) == list:
        state = list(bin_str)
        return normalizza(np.array(state))
    elif type(bin_str) == int:
        state = np.random.rand(bin_str)
        return normalizza(state)
    else:
        return [1]

def Idt(n):
    if n == 1:
        return I
    else:
        return np.kron(I,Idt(n-1))

# Normalizzazione del vettore np.linalg.norm(x)
def normalizza(v):
    return v/np.linalg.norm(v)

def Had(n):
    if n == 1:
        return H
    else:
        return np.kron(H, Had(n-1)) # prodotto tensoriale, np.matmul è quello riga per colonna

# misurazione di un vettore
def counts(v):
    print("COUNTS:")
    N = len(v)
    n = int(np.log2(N))
    formatstr = "{:0>"+str(n)+"b}"
    for i in range(N):
        if v[i] > 0:
            print('- {}, P: {:.2f}%'.format(formatstr.format(i), (v[i]**2)*100))

# CX with many controls
def mcx(n):
    M = Idt(n)
    M[-2], M[-1] = M[-1].copy(), M[-2].copy()
    return M


def gcx(c,t,n):
    mat = Idt(n)
    formatstr = "{:0>"+str(n)+"b}"
    for q in range(2**n):
        v = formatstr.format(q)
        if(v[c] == "0" and v[t] == "0"):
            b = [c for c in v]
            b[c] = "1"
            control = int(''.join(b),2)
            b[t] = "1"
            target = int(''.join(b),2)
            mat[control], mat[target] = mat[target].copy(), mat[control].copy()
    return mat


def gccx(c1,c2,t,n):
    mat = Idt(n)
    formatstr = "{:0>"+str(n)+"b}"
    for q in range(2**n):
        v = formatstr.format(q)
        if(v[c1] == "0" and v[c2] == "0" and v[t] == "0"):
            b = [c for c in v]
            b[c1] = "1"
            b[c2] = "1"
            control = int(''.join(b),2)
            b[t] = "1"
            target = int(''.join(b),2)
            mat[control], mat[target] = mat[target].copy(), mat[control].copy()
    return mat

def gSwap(r1,r2,n):
    M = Idt(n)
    CX1 = gcx(r2,r1,n)
    CX2 = gcx(r1,r2,n)
    CX3 = gcx(r2,r1,n)
    M = np.matmul(CX1,CX2)
    M = np.matmul(M,CX3)
    #M[r1], M[r2] = M[r2].copy(), M[r1].copy()
    return M

# tensor product
def tp(ql):
    v = ql[0]
    for i in range(1,len(ql)):
        v = np.kron(v, ql[i])
    return v


def halfAdder(b0,b1):
    inp0 = get_state(str(b0))
    inp1 = get_state(str(b1))
    out0 = out1 = get_state("0")
    
    a1 = tp([inp0, inp1, out0, out1])
    a2 = np.matmul(gcx(0,2,4), a1)
    a3 = np.matmul(gcx(1,2,4), a2)
    a4 = np.matmul(gccx(0,1,3,4), a3)
    
    counts(a4)

def measure(qubit):
    if sum(qubit) == 1:
        if qubit[-1] == 1:
            return 1
        else:
            return 0
    else:
        return random.randint(0,1)

X = np.array([[0,1],[1,0]])
Z = np.array([[1,0],[0,-1]])
H = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
I = np.array([[1,0],[0,1]])

# TOFFOLI GATE OR CCX
Tof = Idt(3)
Tof[6], Tof[7] = Tof[7].copy(), Tof[6].copy()
Tof = np.array(Tof)

# Controlled NOT Gate
CX = Idt(2)
CX[2], CX[3] = CX[3].copy(), CX[2].copy()
CX = np.array(CX)

# Reversed Controlled NOT Gate
RCX = Idt(2)
RCX[1], RCX[3] = RCX[3].copy(), RCX[1].copy()
RCX = np.array(RCX)

SWAP = Idt(2)
SWAP[1], SWAP[2] = SWAP[2].copy(), SWAP[1].copy()


