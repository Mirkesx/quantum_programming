#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:49:15 2021

@author: mc
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
import quantum_circuits as qcl

# Input qbit e numero qbit da misurare, 4 e 2 per half adder
circuit = QuantumCircuit(4,2)

# Possiamo creare un circuito a partire dall'aggregazione di più qbit definiti come registri
# qr = QuantumRegister(3,"q")
# anc = QuantumRegister(2,"ancilla")
# cr = ClassicalRegister(2, "c")
# circuit = QuantumCircuit(qr,anc, cr)

# circuit.barrier() linea verticale tratteggiata
# circuit.barrier(qr) barriera solo ad alcuni registri come qr nell'esempio


# circuit.x(0) applica X alla linea di qbit passata come parametro, possiamo usare anche indicare i registri (o alcuni di essi con slice)
# circuit.h(qbit_id) hadamard
# circuit.cx(qbit_id, target_id) C-NOT
# circuit.ccx(qbit1_id, qbit2_id, target_id) CC-NOT

# circuit.measure(qbit_id, classical_qbit_id) Misura il primo e lo posiziona nel bit classico
# circuit.measure_all() li misura tutti e viene creata una linea di misurazione apposita per poter gestire questa misurazione 


simulator = QasmSimulator()

compiled_circuit = transpile(circuit, simulator)


job = simulator.run(compiled_circuit, shots=1000)

result = job.result()

#qcl.draw_circuit(circuit)

counts = result.get_counts(compiled_circuit)

#qcl.counts(counts)

'''halfAdder
inp = QuantumRegister(2,"input")
out = QuantumRegister(2,"output")
cr = ClassicalRegister(2, "c")

circuit = QuantumCircuit(inp, out, cr)

#codifica dell'input
circuit.cx(inp[0]) #<- impongo il primo bit ad 1
circuit.cx(inp[1]) #<- impongo il secondo bit ad 1

#modellazione del circuito
circuit.barrier()
circuit.cx(inp[0], out[0])
circuit.cx(inp[1], out[0])
circuit.ccx(inp[0],inp[1], out[1])
circuit.barrier()
circuit.measure(out[0], cr[0])
circuit.measure(out[1], cr[1])

'''



'''halfAdder
halfAdder = QuantumCircuit(4)
halfAdder.cx(0,2)
halfAdder.cx(1,2)
halfAdder.ccx0,1,3)
hag = halfAdder.to_gate() #permette di transformare il nostro circuito in un gate
# ----

circuit = QuantumCircuit(4,2)

#codifica dell'input
circuit.barrier()
circuit.cx(0) #<- impongo il primo bit ad 1
circuit.cx(1) #<- impongo il secondo bit ad 1
circuit.barrier()

# unire halfAdder

#1) circuit = circuit + halfAdder devono avere la stessa dimensione in inoput
#2) circuit.compose(circ, [lines]) Concatena un circuito ed è possibile indicare in quali righe effettuare la composizione (l'ordine nella lista è importante)
# il primo potrebbe essere un gate
circuit = circuit.compose(halfAdder, [0,1,2,3]) # invertibile indicando [3,2,1,0]


#modellazione del circuito
circuit.barrier()
circuit.measure(2,0)
circuit.measure(3,1)

'''