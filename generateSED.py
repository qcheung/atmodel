import const
import numpy as np
import excel
import cal
import plotter
'''
#constant_NGC_958
a_radio = -0.200
Td = 26.9 #k
beta = 1.28
a_high = -2.04
v_radio = 0.14*10**12 #Hz
v_midIR = 3.2*10**12 #Hz

'''
#contant_Mrk_231
a_radio = -0.365
Td = 50.4
beta = 1.21
a_high = -1.56
v_radio = 0.24*10**12 #Hz
v_midIR =  4.8*10**12 #Hz
c = [0.877, 0.991, 0.959]

#generate SED
def SED(freq):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        if v0 < v_radio:
            f = c[0]*v0**a_radio
        elif v0 < v_midIR:
            f = c[1]*v0**beta * (2 * const.h * v0**3 / const.c**2) * ((np.exp(const.h * v0 / (const.k * Td))-1)**(-1))
        else:
            f = c[2]*v0**a_high
        result.append(f)
    return result
        
#xw = excel.ExcelWriter("/home/dave/SED_generate.xlsx")
freq_cm = np.array(cal.generate_freq(start = 0.001, step = 0.005, stop = 30))
#xw.write_col("freq/cm^-1", freq_cm)
freq_hz = 3*10**10/freq_cm
#xw.write_col("freq/Hz", freq_hz)
freq_thz = freq_hz*10**(-12)
#xw.write_col("freq/THz", freq_thz)
f = SED(freq_hz)
#xw.write_col("Intensity", f)
#xw.save()

plotter.loglogplot(freq_thz, f)
