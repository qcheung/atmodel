import gc, const, plotter, file_refs
import numpy as np
from scipy import interpolate
from excel import ExcelReader

#bling_sub is for: CIB, Galactic Emission, and Zodiacal Emission
def bling_sub(freq, temp, resol):
    resol = float(resol)
    f = interpolate.InterpolatedUnivariateSpline(freq, temp, k=1)
    step_size = 1.5e5
    c = 2 * const.h * const.k * step_size 
    int_range_length = freq/2/resol
    int_range = np.zeros((len(freq), 2))
    int_range[:,0]=freq - int_range_length
    int_range[:,1]=freq + int_range_length

    ranges = (np.arange(*(list(i)+[step_size])) for i in int_range) # increasing this step size smooths plot

    result = np.array([c*np.sum(i*f(i)) for i in ranges])
    print "result is ", result
    return result
    # POSSIBLE ISSUES: the mode=2, step size, data files

#bling_Cosmic Microwave Background
def bling_CMB(freq, resol):
    result = []
    freq = np.array(freq, dtype='float')
    for i, v in enumerate(freq):
        i_a = int(i - v / (3e10)/((2 * resol * 0.1)))
        i_b = int(i + v / (3e10)/ ((2 * resol * 0.1)))
        if i_a <= 0:
            i_a = 0
        if i_b > len(freq):
            i_b = len(freq)

        v0 = np.array(freq[i_a:i_b])
##        values = const.h*6e9*np.sum(v0**2/np.exp(v0/const.k/const.T - 1))
        denom = np.exp((const.h * np.sum(v0))/(const.k * const.T)) - 1
        values = 2 * const.h * (np.sum(v0 ** 3))/(const.c ** 2)/denom
        result.append(values)
    print np.array(result)
    return np.array(result)
    
#bling_Atmospheric Radiance
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

#bling_Thermal Mirror Emission
def bling_TME(freq, resol, sigma, mirror_temp):
    result = []
    for i in range(len(freq)):
        v = freq[i]
        offset = v/(3*10**10*2*resol*0.1)
        i_a = int(i - offset) if i >= offset else 0
        i_b = int(i + offset) if len(freq) - offset >= i else len(freq)
        v0 = np.array(freq[i_a:i_b])
        v0 = v0**2.5/np.exp(const.h*v0/const.k/mirror_temp - 1)
        result.append(24e9*const.h**2*(np.pi*const.epsilon/sigma)**0.5*np.sum(v0))
    return np.array(result)

#Limiting_Flux
def LF(freq, d, resol, ts):
    return ts*resol/(2*np.pi*(d/2)**2*freq)

#Integration_Time
def IT(freq, bling_TOT, ratio, ts):
    return (bling_TOT*ratio/ts)**2

    
#Total_Signal
def TS(freq, inte, tau, d, resol):
    try: assert len(freq)==len(tau)
    except AssertionError:
        raise ValueError("The two arrays must have the same length!")
    freq = np.array(freq, dtype="float")
    inte = np.abs(np.array(inte, dtype="float"))
    tau = np.abs(np.array(tau, dtype="float"))
    
    f = interpolate.InterpolatedUnivariateSpline(freq, inte, k=1)
    g = interpolate.InterpolatedUnivariateSpline(freq, tau, k=1)  
    
    inte_resol = 1000.0
    step_size = 0.1 * 3 * 10 ** 10 / inte_resol   #characterize the level of details wanted from interpolation. 
    c = np.pi*(d/2.0)**2*step_size
    int_range_length = freq/2/resol
    int_range = np.zeros((len(freq), 2))
    int_range[:,0]=freq - int_range_length
    int_range[:,1]=freq + int_range_length

    ranges = (np.arange(*(list(i)+[step_size])) for i in int_range)

    return np.array([c*np.sum(f(i)*g(i)) for i in ranges])
