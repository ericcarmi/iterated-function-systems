'''
An Iterated Function System (IFS) module

Functions:
    get:  returns IFS from name as lists of matrices, vectors, probabilities
    rand: returns Nx2 array from random/chaos game method
    det:  returns Nx2 array from deteriminstic iteration

To synthesize a custom IFS, the shapes must match
A : nxn
T : nx1
p : n
T must be a row vector to match A, but p can be a list



Deterministic fern doesn't look good because proportions are off
In random, they are selected based on probability
If selection isn't equal, how to pick with deterministic algorithm?
Just split up the input and apply a certain number based on ratios?

p = [0.01, 0.85, 0.07, 0.07]
With 100 points, A[0] is used once, A[1] 85 times, A[2], A[3] 7 times
That still doesn't make sense...
The IFS converges, should all be applied until change is small?


length for fern IFS
L0 = initial length
L1 = L0*4 + 1
L2 = L1*4 + 1 = (L0*4 + 1)*4 + 1   = L0*16 + 4 + 1
L3 = L2*4 + 1 = (L0*16 + 5)*4 + 1  = L0*64 + 20 + 1
L4 = L3*4 + 1 = (L0*64 + 21)*4 + 1 = L0*256 + 84 + 1
L5 = L4*4 + 1 = (L0*256+ 85)*4 + 1 = L0*1024 + 340 + 1


Ln = L0*4**n + ...
Other sequence is different...it's similar to wavelet length



'''

from numpy import array,pi,sin,cos,sqrt,linspace,zeros,concatenate
import its

def get(name):
    '''
    Input a string corresponding to an IFS name
    Below are the names, before the colon, which can be passed to this function
    - Sierpinski, sierp       : Beyond the tri-force
    - Binary tree, tree       : Branching, rotation, scaling
    - Barnsley fern, fern     : "Fractals Everywhere" is a must read!
    - Heighway dragon, dragon : The twindragon is two of these tiled together
    '''

    if type(name) is not str:
        raise TypeError("Input type must be a string")

    if name == '':
        raise ValueError("Input cannot be empty")

    # Convert to lowercase
    name = name.lower()
    # If input with spaces, get rid of them
    splitname = name.split(' ')
    if len(splitname) > 1:
        name = ''
        for i in splitname:
            name += i

    if name in ['sierpinski', 'sierp']:
        a=[0.5,0.5,0.5]
        b=[0,0,0]
        c=[0,0,0]
        d=[0.5,0.5,0.5]
        E=[0,0,0.5]
        F=[0.5,0,0]
        A1 = array(([a[0], b[0]], [c[0], d[0]]))
        A2 = array(([a[1], b[1]], [c[1], d[1]]))
        A3 = array(([a[2], b[2]], [c[2], d[2]]))
        T1 = array(([E[0]],[F[0]]))
        T2 = array(([E[1]],[F[1]]))
        T3 = array(([E[2]],[F[2]]))
        p=[1/3.,1/3.,1/3.]
        A=[A2,A3,A1] # Swapped to make index correspond to address
        T=[T1,T2,T3]
        return A,T,p

    elif name in ["tree", "binarytree"]:
        a=[0,0.42,0.42,0.1]
        b=[0,-0.42,0.42,0]
        c=[0,0.42,-0.42,0]
        d=[0.5,0.42,0.42,0.1]
        E=[0,0,0,0]
        F=[0,0.2,0.2,0.2]
        p=[0.05,0.4,0.4,0.15]

        A1 = array(([a[0], b[0]], [c[0], d[0] ]))
        A2 = array(([a[1], b[1]], [c[1], d[1] ]))
        A3 = array(([a[2], b[2]], [c[2], d[2] ]))
        A4 = array(([a[3], b[3]], [c[3], d[3] ]))
        T1 = array(([E[0]],[F[0]]))
        T2 = array(([E[1]],[F[1]]))
        T3 = array(([E[2]],[F[2]]))
        T4 = array(([E[3]],[F[3]]))
        A=[A1,A2,A3,A4]
        T=[T1,T2,T3,T4]
        return A,T,p

    elif name in ["barnsley","fern"]:
        a=[0,0.85,0.2,-0.15]
        b=[0,0.04,-0.26,0.28]
        c=[0,-0.04,0.23,0.26]
        d=[0.16,0.85,0.22,0.24]
        E=[0,0,0,0]
        F=[0,1.6,1.6,0.44]
        p=[0.01,0.85,0.07,0.07]

        A1 = array(([a[0], b[0]], [c[0], d[0] ]))
        A2 = array(([a[1], b[1]], [c[1], d[1] ]))
        A3 = array(([a[2], b[2]], [c[2], d[2] ]))
        A4 = array(([a[3], b[3]], [c[3], d[3] ]))
        T1 = array(([E[0]],[F[0]]))
        T2 = array(([E[1]],[F[1]]))
        T3 = array(([E[2]],[F[2]]))
        T4 = array(([E[3]],[F[3]]))
        A=[A1,A2,A3,A4]
        T=[T1,T2,T3,T4]
        return A,T,p

    elif name in ["dragon","heighwaydragon"]:
        x = 0.5
        A1 = array(([x, -x],  [x, x]))
        A2 = array(([-x, -x], [x, -x]))
        T1 = array(([0] ,[0]))
        T2 = array(([1] ,[0]))
        A=[A1,A2]
        T=[T1,T2]
        p=[0.5,0.5]
        return A,T,p

    else:
        print("Did not input a valid IFS name")
        return


def rand(A,T,p,numpoints=1000,z0=0):
    '''
    Random/chaos game algorithm
    z = rand(A,T,p)
    returns array with shape (numpoints,2)
    '''
    z = zeros((numpoints,2))
    z[0] = [0,z0]
    for k in range(1,numpoints):
        z0 = z[k-1]
        z0.shape = (2,1)
        r = its.sample(p)
        z0 = A[r] @ z0 + T[r]
        z[k] = z0[:,0]  
    return z



def det(A,T,numiter=5,z0=1):
    '''
    The deterministic algorithm
    z = det(A,T)
    '''
    La = len(A)
    z = zeros((1,2))
    z[0] = [0,z0]
    i1 = 0
    i2 = 1
    for i in range(numiter):
        q = zeros(((i2-i1)*La*4,2))
        c = 0
        for w in z[i1:i2]:
            w.shape = (2,1)
            for i in range(La):
                q[c] = (A[i] @ w + T[i])[:,0]
                c += 1
        z = concatenate((z,q))
        i1 = i2
        i2 += c
        
    return z
