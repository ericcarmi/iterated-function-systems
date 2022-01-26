from numpy import random,abs, cumsum, array, argmax
from random import uniform

def sample(pdf,which=True):
    '''
    Input a 1 dimensional arbitrary probability density function
    Returns the index by default, set which to 0 to return the value
    '''
    pdf = array(pdf)
    cdf = cumsum(pdf/sum(pdf))
    n = argmax(cdf >= uniform(0,1))
    if which:
        return n
    return pdf[n]
