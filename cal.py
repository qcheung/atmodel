import const
import numpy as np
import scipy.integrate as integrate
import plotter

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
def bling_TME(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * const.T))-1))
        epsilon = (16 * np.pi * v0 * const.epsilon / const.sigma)**(0.5)
        t0 = epsilon * I * const.c**2 / (const.k * v0**2)
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result
    
#bing_Atmospheric_Radiance


#bling_Zodiacal_Emission
def bling_ZE(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        t0 = temp[i]
        result.append(const.h * const.k * v0 * t0 * 2 * v0 / resol)
    return result

#bling_TOT
   
    
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
#testing 
x = range(100)
y = bling_by_temperature(x,range(100),5)
plotter.loglogplot(x, y)