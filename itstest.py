'''
Test for comparing my implementation of random sampling in "its.py" to choice() from pylab
'''

from time import time
from its import sample
from numpy import linspace
from pylab import choice,randint

print("\n\n------Test for speed of inverse transform sampling (ITS) vs. choice------\n\n")

N = 100000
plen = 1000

print("\nRunning", N, "function calls to average generating samples from a distribution of size ", plen)

k = linspace(0,plen-1,plen,dtype=int)
p = randint(0,plen,plen)
p = p / sum(p)

T1 = 0
for i in range(N):
    start = time()
    r = sample(p)
    end = time()
    T1 += end-start
print("Average time to compute using its.sample():", T1 / N)

T2 = 0
for i in range(N):
    start = time()
    r = choice(k,p=p)
    end = time()
    T2 += end-start
    
print("Average time to compute using choice():", T2 / N)
if T2 > T1: print("Choice is faster by a factor of ", T2/T1)
elif T2 < T1: print("ITS is faster by a factor of ", T1/T2)
elif T2 == T1: print("It's a tie!")

print("\n\n")
