import const
import numpy as np
import scipy.integrate as integrate
import plotter

#generate frequency list
def generate_freq(start = 0.05, stop = 2005, step=0.1):
    i = start
    result = []
    while i < stop:
        result.append(i)	
        i += step
    return result

#bling_Cosmology_Infrared_Backgrond   
def bling_CIB(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return np.array(result)
    
#bling_Cosmology_Microwave_Backgrond
def bling_CMB(freq, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * const.T))-1))
        t0 = I * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0*t0 * 2 * v0 / resol)
    return np.array(result)
    
#bling_Galactic_Emission       
def bling_GE(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return np.array(result)
  
#bling_Thermal Mirror Emission
def bling_TME(freq, resol, sigma, mirror_temp):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * mirror_temp))-1))
        epsilon = (16 * np.pi * v0 * const.epsilon / sigma)**(0.5)
        t0 = epsilon * I * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return np.array(result)
    
#bing_Atmospheric_Radiance
def bling_AR(freq, rad, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = rad[i]
        t0 = i0 * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return np.array(result)

#bling_Zodiacal_Emission
def bling_ZE(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return np.array(result)

#Total_Signal
def TS(freq, inte, tau, d, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = inte[i]
        tau0 = tau[i]
        p0 = np.pi * (d / 2)**2 * tau0 * i0 * 2 * v0 / resol
        result.append(p0)
    return np.array(result)

#Limiting_Flux
def LF(freq, inte, tau, d, resol, ts):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = inte[i]
        tau0 = tau[i]
        p0 = ts[i]
        result.append((p0 *resol) / (2 * np.pi * (d / 2)**2 * v0))
    return np.array(result)

#Integration_Time
def IT(freq, bling, ratio, inte, tau, d):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        n0 = bling[i]
        tau0 = tau[i]
        p0 = TS(freq, inte, tau, d, resol)
        result.append((n0 * ratio / p0)**2)
    return np.array(result)

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
    print np.transpose(result)
    return np.transpose(result)

