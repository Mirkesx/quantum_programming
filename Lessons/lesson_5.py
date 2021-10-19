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

X = np.array([[0,1],[1,0]])
Z = np.array([[1,0],[0,-1]])
H = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
I = np.array([[1,0],[0,1]])
Tof = Idt(3)
Tof[6,7] = Tof[7,6] = 1
Tof[6,6] = Tof[7,7] = 1
Tof = np.array(Tof)

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