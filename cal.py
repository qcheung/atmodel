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
        result.append(const.h * const.k * v0*t0 * 2 * v0 / resol)
    return result
    
#bling_Cosmology_Microwave_Backgrond
def bling_CMB(freq, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * const.T))-1))
        t0 = I * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0*t0 * 2 * v0 / resol)
        
    return result
    
#bling_Galactic_Emission       
def bling_GE(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result
  
#bling_Thermal Mirror Emission
def bling_TME(freq, temp, resol, sigma, t):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * t))-1))
        epsilon = (16 * np.pi * v0 * const.epsilon / sigma)**(0.5)
        t0 = epsilon * I * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result
    
#bing_Atmospheric_Radiance
def bling_AR(freq, rad, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = rad[i]
        t0 = i0 * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result    

#bling_Zodiacal_Emission
def bling_ZE(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result

#Total_Signal
def TS(freq, inte, tao, d, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = inte[i]
        tao0 = tao[i]
        p0 = np.pi * (d / 2)**2 * tao0 * i0 * 2 * v0 / resol
        result.append(p0)
    return result

#Limiting_Flux
def LF(freq, inte, tao, d, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = inte[i]
        tao0 = tao[i]
        p0 = TS(freq, inte, tao, d)
        result.append((p0 *resol) / (2 * np.pi * (d / 2)**2 * v0))
    return result

#Integration_Time
def IT(freq, bling, ratio, inte, tao, d):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        n0 = bling[i]
        tao0 = tao[i]
        p0 = TS(freq, inte, tao, d)
        result.append((n0 * ratio / p0)**2)
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
    print np.transpose(result)
    return np.transpose(result)

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
        freq_begin = v0 - v0/float(resol)
        freq_end = v0 + v0/float(resol)
        temp_data = trancate(data, freq_begin, freq_end)
        temp_freq = temp_data[0]
        temp_temp = temp_data[1]
        integral = const.h * const.k * temp_freq * temp_temp
        result.append(integrate.trapz(integral, temp_freq)**(0.5))
    return result
