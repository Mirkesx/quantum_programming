#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 16:19:21 2022

@author: mc
"""

import numpy as np
import random


def get_state(s):
    n = len(s)
    state = np.array([0] * 2**n)
    s_int = int(s, 2)
    state[s_int] = 1
    return state

H2 = (1/np.sqrt(2)) * np.array([[1,1],
                                [1,-1]])


def H(n):
    if n == 1:
        return H2
    
    return np.kron(H2, H(n-1))


def Id(n):
    I = np.array([ [0] * 2**n ] * 2**n)
    for i in range(2**n):
        I[i][i] = 1
    return np.array(I)

def Ref(n):
    # 2Pa - I, a = |+>, Pa = |a><a|
    a = 1/np.sqrt(2**n) * np.array([1] * 2**n)
    a = np.array([list(a)])    
    
    Pa = np.matmul(np.transpose(a), a)
    
    return 2*Pa - Id(n)

def PhaseOracle(sol, n):
    Ps = Id(n)
    for x in sol:
        i = int(x, 2)
        Ps[i,i] = -1
    return Ps


def Grove(sol):
    n = len(sol[0])
    N = 2**n
    M = len(sol)
    
    t = int((np.pi/4) * np.sqrt(N/M))
    
    Refs = Ref(n)
    Ps = PhaseOracle(sol, n)
    
    # |a0>
    
    a0 = get_state("0"*n)
    print("|ao> = {}".format(a0))
    
    a1 = np.matmul(H(n), a0)
    print("|a1> = {}".format(a1))
    
    for i in range(t):
        a1 = np.matmul(Ps, a1)
        #print("Uf => |a1'> = {}".format(a1))
        a1 = np.matmul(Refs, a1)
        #print("Ref => |a1'> = {}".format(a1))

    print("|a2> = {}".format(a1))