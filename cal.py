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
#bling_Galactic_Emission 
#bling_Zodiacal_Emission
def bling_sub(freq, temp, resol):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        i_start = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        i_end = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        if i_start <= 0:
            i_start = 0
        if i_end > len(freq):
            i_end = len(freq)
        p0 = 0
        for j in range(i_start, i_end):
            v0 = freq[j]
            t0 = temp[j]
            p0 = p0 + const.h * const.k * v0 * t0 * 0.1*10**10*3
        result.append(p0)
    return np.array(result)
    
#bling_Cosmology_Microwave_Backgrond
def bling_CMB(freq, resol):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        i_start = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        i_end = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        if i_start <= 0:
            i_start = 0
        if i_end > len(freq):
            i_end = len(freq)
        p0 = 0
        for j in range(i_start, i_end):
            v0 = freq[j]
            I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * const.T))-1))
            t0 = I * const.c**2 / (const.k * v0**2)
            p0 = p0 + const.h * const.k * v0 * t0 * 0.1*10**10*3
        result.append(p0)
    return np.array(result)
  
#bling_Thermal Mirror Emission
def bling_TME(freq, resol, sigma, mirror_temp):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        i_start = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        i_end = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        if i_start <= 0:
            i_start = 0
        if i_end > len(freq):
            i_end = len(freq)
        p0 = 0
        for j in range(i_start, i_end):
            v0 = freq[j]
            I = 2 * const.h * v0**3 / (const.c**2 * (np.exp((const.h * v0) / (const.k * mirror_temp))-1))
            epsilon = (16 * np.pi * v0 * const.epsilon / sigma)**(0.5)
            t0 = epsilon * I * const.c**2 / (const.k * v0**2)
            p0 = p0 + const.h * const.k * v0 * t0 * 0.1*10**10*3
        result.append(p0)
    return np.array(result)
    
#bing_Atmospheric_Radiance
def bling_AR(freq, rad, resol):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        i_start = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        i_end = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        if i_start <= 0:
            i_start = 0
        if i_end > len(freq):
            i_end = len(freq)
        p0 = 0
        for j in range(i_start, i_end):
            v0 = freq[j]
            i0 = rad[j]
            t0 = i0 * const.c**2 / (const.k * v0**2)
            p0 = p0 + const.h * const.k * v0 * t0 * 0.1*10**10*3
        result.append(p0)
    return np.array(result)

#bling_Zodiacal_Emission

#Total_Signal

#Limiting_Flux
def LF(freq, d, resol, ts):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        p0 = ts[i]
        result.append((p0 *resol) / (2 * np.pi * (d / 2)**2 * v0))
    return np.array(result)

#Integration_Time
def IT(freq, bling_TOT, ratio, ts):
    result = []
    for i in range(len(freq)):
        n0 = bling_TOT[i]
        p0 = ts[i]
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

#Total_Signal
def TS(freq, inte, tau, d, resol):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        #i_start = int((v - v/2/resol -0.05)/0.1 )
        i_start = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        #i_end = int((v + v/2/resol -0.05)/0.1 )
        i_end = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        
        if i_start <= 0:
            i_start = 0
        if i_end > len(freq):
            i_end = len(freq)

        p0 = 0
        for j in range(i_start, i_end):
            v0 = freq[j]
            i0 = inte[j]
            tau0 = tau[j]
            p0 = p0 + np.pi * (float(d) / 2)**2 * tau0 * i0 * 0.1*10**10*3
        result.append(p0)
    return np.array(result)
'''
def TS(freq, inte, tau, d, resol):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        i0 = inte[i]
        tau0 = tau[i]
        p0 = np.pi * (d / 2)**2 * tau0 * i0 * 2 * v0 / resol
        result.append(p0)
    return np.array(result)
'''

#result = TS([0.05+0.1*i for i in range(50,100)], [10 for i in range(50)],[1 for i in range(50)],1,3)
#plotter.loglogplot([0.05+0.1*i for i in range(50,100)],result)
