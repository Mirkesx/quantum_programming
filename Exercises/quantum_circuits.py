#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:50:52 2021

@author: mc
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
import os
import time


# raise up the quality of the inline plots
dpi = 200
mpl.rcParams['figure.dpi']= dpi
mpl.rc("savefig", dpi=dpi)

def draw_circuit(qc):
    now = int(time.time())
    filepath = '{}.png'.format(now)
    figure = qc.draw(output="mpl")
    figure.savefig( filepath )
    img = mpimg.imread( filepath )
    plt.axis('off')
    plt.grid(b=None)
    plt.imshow(img)
    os.remove( filepath )
    
# returns a list of qbits from a register
def get_qbits(list_registers):
    list_qbits = []
    for register in list_registers:
        list_qbits.extend([qbit for qbit in register] if type(register) == QuantumRegister else [])
    return list_qbits

def reformat_counts(counts, n, t=0):
    keys = [key for key in counts.keys()]
    keys.sort()
    new_counts = {
        key: round(counts[key]/n * 100, 2) for key in keys if counts[key]/n > t
    }
    return new_counts
    
    