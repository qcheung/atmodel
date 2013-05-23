import const
import numpy as np
import scipy.integrate as spint

def ta(freq, intensity):
    f = np.array(freq)
    i = np.array(intensity)
    ta = i*(const.c)**2/(const.k*(f**2))
    return ta

def bling(freq, intensity, resol):
    f = np.array(freq)
    t = ta(freq, intensity)
    integral = const.h * const.k * f * t
    result = spint.simps(integral, freq)
    return result

def trancate(freq, start, end):
    