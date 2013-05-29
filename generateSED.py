#constant_NGC_958
a_radio = -0.200
Td = 26.9
beta = 1.28
a_high = -2.04
v_radio = 0.14 #THz
v_migIR = 3.2 #THz

'''
#contant_Mrk_231
a_radio = -0.365
Td = 50.4
beta = 1.21
a_high = -1.56
v_radio = 0.24 #THz
v_migIR = 4.8 #THz
'''

#generate SED
def SED(freq):
    result = []
    for i in range(len(freq)):
    v0 = freq[i]
    if v0 <= v_radio:
      f = v0**a_radio
      else if v0 <= v_midIR:
        f = v0**beta * (2 * const.h * v0**3 / const.c**2) * ((np.exp(const.h * v0 / (const.k * Td))-1)**(-1)
      else:
        f = v0**a_high
        
        
