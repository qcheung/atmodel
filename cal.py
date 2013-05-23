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
        freq_begin = v0 - v0/resol
        freq_end = v0 + v0/resol
        data = [freq,intensity]
        data = trancate(data, freq_begin, freq_end)
        f = data[0]
        i = data[1]
        t = ta(f,i)
        integral = const.h * const.k * f * i * t
        result.append(integrate.simps(integral, i)**(0.5))
    return result
def bling_by_temperature(freq, temp, resol):
    result = []
    data = [freq,temp]
    for v0 in freq:
        freq_begin = v0 - v0/resol
        freq_end = v0 + v0/resol
        temp_data = trancate(data, freq_begin, freq_end)
        temp_freq = temp_data[0]
        temp_temp = temp_data[1]
        integral = const.h * const.k * temp_freq * temp_temp
        result.append(integrate.simps(integral, temp_freq)**(0.5))
    return result
    
def bling_Galactic_Emission(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        freq_begin = v0 - v0/resol
        freq_end = v0 + v0/resol
        result = const.h * const.k * v0 * t0 * (freq_end - freq_begin)
    return result

def trancate(data, start, end):
    '''
    Used to trancate an array based on frequency
    ''' 
    data = np.transpose(data)
    result = []
    for x in data:
        if x[0] > end:
            break
        if x[0] >= start:
            result.append(x)
    return np.transpose(result)

#print bling_by_temperature([1,2,3,4,5],[1,2,3,4,5],100)
