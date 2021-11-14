import numpy as np
import lesson_7 as qc
import random

def getPair(entangled=False, pair="11"):
    q = qc.get_state(pair)
    if entangled:
        op1 = np.kron(qc.H, qc.I)
        op = np.matmul(qc.CX, op1)
        q = np.matmul(op, q)
    return q

A = [
    None,
    qc.Z,
    qc.X,
    qc.H     
]

B = [
    None,
    qc.Z,
    (qc.Z - qc.X)/np.sqrt(2),
    qc.H     
]

def projective_measurement(q, M):
    return np.matmul(q, np.matmul(M, q))


def measure(qubit):
    if sum(qubit) == 1:
        if qubit[-1] == 1:
            return 1
        else:
            return 0
    else:
        return random.randint(0,1)


def E91(N, interception=False):
    qubits = [ getPair(not interception) for i in range(N) ]
    
    alice_bases = []
    bob_bases = []
    for i in range(N):
        alice_bases.append(random.randint(1,3))
        bob_bases.append(random.randint(1,3))
        
    OkB = [[1,1], [3,3]]
        
    key_list = [ i for i in range(N) if [alice_bases[i], bob_bases[i]] in OkB ]
    
    CHSHB = [ [1,3], [1,2], [2,3], [2,2] ]
    
    CHST_list = [ [i, alice_bases[i], bob_bases[i]] for i in range(N) if [alice_bases[i], bob_bases[i]] in CHSHB ]
    
    CHSHval = 0
    for idx in range(len(CHST_list)):
        [i, a_i, b_j] = CHST_list[idx]
        op = np.kron(A[a_i], B[b_j])
        qubit = qubits[i]
        s = np.matmul(op,qubit)
        CHSHval += -np.matmul(qubit,s) if [a_i, b_j] == [2, 2] else np.matmul(qubit,s)
    
    CHSHval = np.abs(CHSHval*4/len(CHST_list)) if len(CHST_list) > 0 else 0.0
    
    if CHSHval > 2:
        print("CHSH inequaliy test passed with {}".format(CHSHval))
        alice_key = ""
        bob_key = ""
        for i in key_list:
            s = measure(qubits[i])
            alice_key += "{}".format(s)
            bob_key += "{}".format(1 - s)
        print("Alice's secret key is: {}".format(alice_key))
        print("Bob's secret key is: {}".format(bob_key))
    else:
        print("CHSH inequaliy test failed with {}".format(CHSHval))
        