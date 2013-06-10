import gc
import const
import numpy as np
from scipy import interpolate
import plotter
import file_refs
from excel import ExcelReader
gc.disable()

def bling_sub(freq, temp, resol):
    resol = float(resol)
    result = [0]*len(freq)
    f = interpolate.interp1d(freq, temp, kind = 'linear')
    def t(v):
        if v<freq[0]:
            return (temp[1]-temp[0]) / (freq[1]-freq[0]) * (v-freq[0]) + temp[0]
        elif v>freq[-1]:
            return (temp[-1]-temp[-2]) / (freq[-1]-freq[-2]) * (v-freq[-1]) + temp[-1]
        else:
            return f(v)
           
    step_size = 0.1*3*10**10/2    #characterize the level of details wanted from interpolation. 

    for i in range(len(freq)):
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
   
#bling_Cosmology_Infrared_Backgrond  
#bling_Galactic_Emission 
#bling_Zodiacal_Emission
'''
def bling_sub(freq, temp, resol):

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
'''
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
    
#Total_Signal
def TS(freq, inte, tau, d, resol):  
    result = [0]*len(freq)
    print "Interpolating..."
    f = interpolate.interp1d(freq, inte, kind = 'linear')
    g = interpolate.interp1d(freq, tau, kind = 'linear')
    print "Interpolation DONE"
    
    def intensity(v):
        if v<freq[0]:
            return (inte[1]-inte[0]) / float((freq[1]-freq[0])) * (v-freq[0]) + inte[0]
        elif v>freq[-1]:
            return (inte[-1]-inte[-2]) / float((freq[-1]-freq[-2])) * (v-freq[-1]) + inte[-1]
        else:   
            return f(v)
    
    def transmission(v):
        if v<freq[0]:
            return (tau[1]-tau[0]) / float((freq[1]-freq[0])) * (v-freq[0]) + tau[0]
        elif v>freq[-1]:
            return (tau[-1]-tau[-2]) / float((freq[-1]-freq[-2])) * (v-freq[-1]) + tau[-1]
        else:
            return g(v)   
    print "helper function definition. DONE"
    
    inte_resol = 10.0
    step_size = 0.1 * 3 * 10 ** 10 / inte_resol   #characterize the level of details wanted from interpolation. 

    print "Start integration..."
    for i in range(len(freq)):
        v0 = float(freq[i])
        
        inte_range = v0/resol
        inte_start = v0 - inte_range/2
        inte_end = v0 + inte_range/2

        SED = 0.0
        for v in np.arange(inte_start, inte_end, step_size):
            SED +=  3.1416 * (d/2.0)**2 * transmission(v) * intensity(v) * step_size
        result[i] = SED 
        print "Frequency: ",freq[i], " Hz DONE"

    return np.array(result)

def TS2(freq, inte, tau, d, resol):
    '''
    This is to create a super fast linear approximation to the integration to calculate Total Signal
    '''
    for i in range(len(freq)):
        v0 = float(freq[i])
        
        inte_range = v0/resol
        fstart = v0 - inte_range/2   #FLOATING POINT START
        fend = v0 + inte_range/2     #FLOATING POINT END

        SED = 0.0
        if fstart < freq[0]:
            
        inte[1]-inte[0]) / float((freq[1]-freq[0])) * (v-freq[0]) + inte[0]
        istart = int(((fstart + 0.1) - 0.05) / 0.1)     #INTEGAR START -> ON THE RIGHT OF FSTART
        iend = int(((fend - 0.05) / 0.1))                #INTEGAR END -> ON THE LEFT OF FEND

        #integration is then divided into three parts
        #integrate istart -> iend
        
        for j in range(istart, iend):
            integral_1 = 3.1416 * (d/2.0)**2 * inte[j] * tau[j] * step_size
            integral_2 = 3.1416 * (d/2.0)**2 * inte[j+1] * tau[j+1] * step_size
            SED += (inte[j+1] + inte[j])/2 * 0.1
            
        #integrate fstart -> istart
        diff = istart - fstart
        gradient = (inte[istart] - inte[istart-1])/0.1
        SED += gradient * diff + inte[istart]

        #integrate iend -> fend
        diff = fend - iend
        gradient = (inte[iend + 1] - inte[iend])/0.1
        SED += gradient * diff + inte[iend]
        
        #Return result
        result[i] = SED 
        print "Frequency: ",freq[i], " Hz DONE"

    return np.array(result)
    
'''
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
#TESTING
'''
cib_excel = file_refs.CIB_ref
cib = ExcelReader(cib_excel)
cib.set_freq_range(0.05, 100)
freq = cib.read_from_col(1)
temp = cib.read_from_col(4)
bling = bling_sub(freq, temp, 10)

plotter.loglogplot(freq, bling)
'''
#print bling_sub([1,2,3,4,5],[1,2,3,4,5],5)
