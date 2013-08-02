import gc, const, plotter, file_refs
import numpy as np
from scipy import interpolate
from excel import ExcelReader

#bling_sub is for: CIB, Galactic Emission, and Zodiacal Emission
def bling_sub(freq, temp, resol):
    resol = float(resol)
    result = np.zeros(len(freq))
    f = interpolate.interp1d(freq, temp, kind = 'linear')
    def t(v):
        if v<freq[0]:
            return (temp[1]-temp[0]) / (freq[1]-freq[0]) * (v-freq[0]) + temp[0]
        elif v>freq[-1]:
            return (temp[-1]-temp[-2]) / (freq[-1]-freq[-2]) * (v-freq[-1]) + temp[-1]
        else:
            return f(v)
           
    step_size = 1.5e9    #characterize the level of details wanted from interpolation. 

    for i in np.arange(len(freq)):
        v0 = float(freq[i])
        inte_range = v0/resol
        inte_start = v0 - inte_range/2
        inte_end = v0 + inte_range/2

        bling = 0.0
        for v in np.arange(inte_start, inte_end, step_size):
            bling += const.h * const.k * v * t(v) * step_size
        result[i] = bling
        print "This is done: ",i,": ",freq[i]

    return np.array(result)
   
    

#bling_Cosmic_Microwave_Background
def bling_CMB(freq, resol):
    result = []
    for i, v in enumerate(freq):
        i_a = int( i - v / (3e10)/((2 * resol * 0.1))) #question: why do we want this to be integer?
        i_b = int(i + v / (3e10)/ ((2 * resol * 0.1)))
        if i_a <= 0:
            i_a = 0
        if i_b > len(freq):
            i_b = len(freq)

        v0 = freq[i_a:i_b]*int(const.h) #h shouldn't have to be made an integer
        v0_1 = np.array(v0) #create array to square list
        v0_2 = v0_1**2/np.exp(v0_1/const.k/const.T - 1)
        result.append(6e9*np.sum(v0_2))
    return np.array(result)
  
#bling_Thermal Mirror Emission
def bling_TME(freq, resol, sigma, mirror_temp):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        offset = v/(3*10**10*2*resol*0.1)
        i_a = int(i - offset) if i >= offset else 0
        i_b = int(i + offset) if len(freq) - offset >= i else len(freq)
        v0 = freq[i_a:i_b]
        v0 = v0**2.5/np.exp(const.h*v0/const.k/mirrot_temp - 1)
        result.append(24e9*const.h**2*(np.pi*const.epsilon/sigma)**0.5*np.sum(v0))
    return np.array(result)
    
#bling_Atmospheric_Radiance
def bling_AR(freq, rad, resol):
    result = []
    for i, v in enumerate(freq):
        i_a = int( i - v / (3*10**10)/((2 * resol * 0.1)))
        i_b = int(i + v / (3*10**10)/ ((2 * resol * 0.1)))
        if i_a <= 0:
            i_a = 0
        if i_b > len(freq):
            i_b = len(freq)
        rad_array = np.array(rad[i_a:i_b]) #make arrays of lists to divide them
        freq_array = np.array(freq[i_a:i_b])
        t0 = rad_array/freq_array #divide arrays instead of lists
        result.append(const.c**2*const.h*3e9*np.sum(t0))
    return np.array(result)

#Limiting_Flux
def LF(freq, d, resol, ts):
    return ts*resol/(2*np.pi*(d/2)**2*freq)

#Integration_Time
def IT(freq, bling_TOT, ratio, ts):
    return (bling_TOT*ratio/ts)**2

    
#Total_Signal
def TS(freq, inte, tau, d, resol):  
    result = [0]*len(freq)
    print "Interpolating..."
    f = interpolate.InterpolatedUnivariateSpline(freq,inte, k=1)
    g = interpolate.InterpolatedUnivariateSpline(freq,tau, k=1)
    print "Interpolation DONE" 
    
    inte_resol = 1000.0
    step_size = 0.1 * 3 * 10 ** 10 / inte_resol   #characterize the level of details wanted from interpolation. 

    c = 3.1416*(d/2.0)**2*step_size
    print "Start integration..."
    for i in range(len(freq)):
        v0 = float(freq[i])
        
        inte_range = v0/resol
        inte_start = v0 - inte_range/2
        inte_end = v0 + inte_range/2

        x = np.arange(inte_start, inte_end, step_size)
        result[i] = c*np.sum(f(x)*g(x))
        print "Frequency: ",freq[i], " Hz DONE"

    return np.array(result)
