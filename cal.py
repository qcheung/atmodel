import gc, const, plotter, file_refs
import numpy as np
from scipy import interpolate
from excel import ExcelReader

# These calculations reference equations in 2 papers:
# "Limitations on Observing Submillimeter and Far Infrared Galaxies" by Denny
# and
# "Fundamental Limits of Detection in the Far Infrared" by Denny et al

def bling_sub(freq, temp, resol):  #calculates BLING(squared) for "Cosmic Infrared Background", "Galactic Emission", and/or "Zodiacal Emission"
##    What will be done: 1) Interpolate temperature vs. frequency
##                       2) Calculate integration constants and integration range
##                       3) Calculate BLING(squared) from antenna temperature
## 1) Interpolate temperature vs. frequency
    f = interpolate.InterpolatedUnivariateSpline(freq, temp, k=1) #linear interpolation of "temp" vs. "freq"

## 2) Calculate integration constants and integration range
    resol = float(resol)  #ensure "resol" is a float not an integer
    step_size = 1.5e5  #characterize the level of details wanted from interpolation
        #decreasing "step_size" can lose smoothness of plot and increasing "step_size" lengthens calculation time
    c = 2 * const.h * const.k * step_size  #2 is number of modes, constants come from equation 2.15 in Denny(without the radical), "step_size" is the increment of the Riemann sum
    int_range = np.zeros((len(freq), 2)) #create 2 by (length of frequency range) array full of 0's to be replaced with values
    int_range_length = freq/2/resol  #2nd term in integration bounds from equation 2.15 in Denny
    int_range[:,0]=freq - int_range_length  #fill up 1st column of 0's array with bottom integration bound from equation 2.15 in Denny
    int_range[:,1]=freq + int_range_length  #fill up 2nd column of 0's array with top integration bound from equation 2.15 in Denny

    ranges = (np.arange(*(list(i)+[step_size])) for i in int_range)  #"i in int_range" refers to each row(which has a start and end to the integration range)
        #for each row, an array is created with values ranging from the starting value to the ending value, in increments of "step_size"

## 3) Calculate BLING(squared from antenna temperature
    blingSUB_squared = np.array([c*np.sum(i*f(i)) for i in ranges])  #"i in ranges" refers to each row(of the bounds plus "step_size") from the array created above
        #for each row, each of the 2 bounds is multiplied by its corresponding temperature from the linear interpolation done at the start and then are summed
        #summing does the integral for each frequency
        #the sum is multiplied by the number of modes, physical constants, and "step_size" which gives the BLING
        #the result should be square rooted but, since the BLINGs are to be added in quadrature, squaring each BLING cancels out the radical
    return blingSUB_squared


def bling_CMB(freq, resol):  #calculates BLING(squared) for "Cosmic Microwave Background"
##    What will be done: 1) Calculate intensity from frequency
##                       2) Calculate antenna temperature from intensity
##                       3) Calculate BLING(squared) from antenna temperature
## 1) Calculate intensity from frequency
    resol = float(resol)  #ensure "resol" is a float not an integer
    freq = np.array(freq, dtype='float')  #ensure "freq" is a float not an integer
    temp = []  #create list to be filled with calculated temperatures
    for v0 in freq:
        denom = np.exp((const.h * v0)/(const.k * const.T)) - 1  #calculate part of the denominator in equation 2.16 in Denny
        intensity = 2 * const.h * (v0 ** 3)/(const.c ** 2)/denom  #calculate intensity from equation 2.16 in Denny

## 2) Calculate antenna temperature from intensity
        antenna_temp = intensity * (const.c ** 2)/(const.k * (v0**2))  #calculate antenna temperature from equation 2.7 in Denny
        temp.append(antenna_temp)  #add calculated temperature to "temp" list
    temp = np.array(temp)  #turn "temp" list into "temp" array

## 3) Calculate BLING(squared) from antenna temperature
    f = interpolate.InterpolatedUnivariateSpline(freq, temp, k=1) #linear interpolation of "temp" vs. "freq"
    step_size = 1.5e5  #characterize the level of details wanted from interpolation
        #decreasing "step_size" can lose smoothness of plot and increasing "step_size" lengthens calculation time
    c = 2 * const.h * const.k * step_size  #2 is number of modes, constants come from equation 2.15 in Denny(without the radical), "step_size" is the increment of the Riemann sum
    int_range = np.zeros((len(freq), 2)) #create 2 by (length of frequency range) array full of 0's to be replaced with values
    int_range_length = freq/2/resol  #2nd term in integration bounds from equation 2.15 in Denny
    int_range[:,0]=freq - int_range_length  #fill up 1st column of 0's array with bottom integration bound from equation 2.15 in Denny
    int_range[:,1]=freq + int_range_length  #fill up 2nd column of 0's array with top integration bound from equation 2.15 in Denny

    ranges = (np.arange(*(list(i)+[step_size])) for i in int_range)  #"i in int_range" refers to each row(which has a start and end to the integration range)
        #for each row, an array is created with values ranging from the starting value to the ending value, in increments of "step_size"

    blingCMB_squared = np.array([c*np.sum(i*f(i)) for i in ranges])  #"i in ranges" refers to each row(of the bounds plus "step_size") from the array created above
        #for each row, each of the 2 bounds is multiplied by its corresponding temperature from the linear interpolation done at the start and then are summed
        #summing does the integral for each frequency
        #the sum is multiplied by the number of modes, physical constants, and "step_size" which gives the BLING
        #the result should be square rooted but, since the BLINGs are to be added in quadrature, squaring each BLING cancels out the radical

    return np.array(blingCMB_squared)

        
def bling_AR(freq, rad, resol):  #calculates BLING(squared) for "Atmospheric Radiance"
##    What will be done: 1) Interpolate radiance vs. frequency
##                       2) Calculate antenna temperature from radiance
##                       3) Calculate BLING(squared) from antenna temperature
## 1) Interpolate radiance vs. frequency
    rad = interpolate.InterpolatedUnivariateSpline(freq, rad, k=1) #linear interpolation of "rad" vs. "freq"

## 2) Calculate antenna temperature from radiance
    temp = []  #create list to be filled with calculated temperatures
    for i in freq:
        antenna_temp = rad(i) * (const.c ** 2)/(const.k * (i**2))  #calculate antenna temperature from equation 2.7 in Denny
        temp.append(antenna_temp)  #add calculated temperature to "temp" list
    temp = np.array(temp)  #turn "temp" list into "temp" array

## 3) Calculate BLING(squared) from antenna temperature
    f = interpolate.InterpolatedUnivariateSpline(freq, temp, k=1) #linear interpolation of "temp" vs. "freq"
    step_size = 1.5e5  #characterize the level of details wanted from interpolation
        #decreasing "step_size" can lose smoothness of plot and increasing "step_size" lengthens calculation time
    c = 2 * const.h * const.k * step_size  #2 is number of modes, constants come from equation 2.15 in Denny(without the radical), "step_size" is the increment of the Riemann sum
    int_range = np.zeros((len(freq), 2)) #create 2 by (length of frequency range) array full of 0's to be replaced with values
    int_range_length = freq/2/resol  #2nd term in integration bounds from equation 2.15 in Denny
    int_range[:,0]=freq - int_range_length  #fill up 1st column of 0's array with bottom integration bound from equation 2.15 in Denny
    int_range[:,1]=freq + int_range_length  #fill up 2nd column of 0's array with top integration bound from equation 2.15 in Denny

    ranges = (np.arange(*(list(i)+[step_size])) for i in int_range)  #"i in int_range" refers to each row(which has a start and end to the integration range)
        #for each row, an array is created with values ranging from the starting value to the ending value, in increments of "step_size"

    blingAR_squared = np.array([c*np.sum(i*f(i)) for i in ranges])  #"i in ranges" refers to each row(of the bounds plus "step_size") from the array created above
        #for each row, each of the 2 bounds is multiplied by its corresponding temperature from the linear interpolation done at the start and then are summed
        #summing does the integral for each frequency
        #the sum is multiplied by the number of modes, physical constants, and "step_size" which gives the BLING
        #the result should be square rooted but, since the BLINGs are to be added in quadrature, squaring each BLING cancels out the radical

    return np.array(blingAR_squared)

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
