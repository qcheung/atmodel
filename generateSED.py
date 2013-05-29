import const
import numpy as np
import excel
import cal
import plotter

#constant_NGC_958
a_radio = -0.200
Td = 26.9
beta = 1.28
a_high = -2.04
v_radio = 0.14 #THz
v_midIR = 3.2 #THz

'''
#contant_Mrk_231
a_radio = -0.365
Td = 50.4
beta = 1.21
a_high = -1.56
v_radio = 0.24 #THz
v_midIR = 4.8 #THz
'''

#generate SED
def SED(freq):
    result = []
    for i in range(len(freq)):
        v0 = freq[i]
        if v0 <= v_radio:
            f = v0**a_radio
        elif v0 <= v_midIR:
            f = v0**beta * (2 * const.h * v0**3 / const.c**2) * ((np.exp(const.h * v0 / (const.k * Td))-1)**(-1))
        else:
            f = v0**a_high
        result.append(f)
    return result
        
xw = excel.ExcelWriter("/home/dave/SED_generate.xlsx")
freq_cm = np.array(cal.generate_freq())
xw.write_col("freq/cm^-1", freq_cm)
freq_hz = 3*10**10/freq_cm
xw.write_col("freq/Hz", freq_hz)
freq_thz = freq_hz*10**(-12)
xw.write_col("freq/THz", freq_thz)
xw.write_col("Intensity", SED(freq_thz))
xw.save()

