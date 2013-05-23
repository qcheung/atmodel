import const
import numpy as np
import scipy.integrate as integrate

def ta(freq, intensity):
    f = np.array(freq)
    i = np.array(intensity)
    ta = i*(const.c)**2/(const.k*(f**2))
    return ta

def bling(freq, intensity, resol):
    result = []
    for v0 in freq:
        int_begin = v0 - v0/resol
        int_end = v0 + v0/resol
        f = np.array(trancate(freq, int_begin, int_end))
        t = ta(freq, intensity)
        integral = const.h * const.k
        result.append(integrate.simps(integral, freq))
    return result

def trancate(arr, start, end):
    result = []
    for x in arr:
        if x > end:
            break
        if x >= start:
            result.append(x)
    return result
