from math import gcd
import random


completed = False
while not completed:
    state = 1
    N = 143
    a = random.randint(2,N-1)
    if gcd(a, N) == 1:
        print("------------------------\na = {}, N = {}".format(a, N))
        mod = a % N
        i = 0
        while mod != 1:
            i+=1
            print("Iterazione {}".format(i))
            state = a * state
            mod = state % N
            print("{}*{} mod {} = {}".format(state, a, N, mod))
        
        r = i    
        print("Finito. Ordine: {}".format(r))
        
        if r % 2 == 0:
            if gcd(a**(int(r/2))-1, N) not in [1, N] and gcd(a**(int(r/2))+1, N) not in [1, N]:
                print("Fattore 1: ", gcd(a**(int(r/2))-1, N) )
                print("Fattore 2: ", gcd(a**(int(r/2))+1, N) )
                completed = True
            else:
                print("Trovata soluzione banale!")
        else:
            print("r è dispari.")
