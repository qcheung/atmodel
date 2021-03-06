'''
Created on May 22, 2013

@author: dave
'''

'Physical Constants'

#general constants
h = 6.63*10**(-34) # J*s
k = 1.38*10**(-23) # J/K
c = 3*10**8 # m/s
T = 2.73 # k

#material constants for Thermal Mirror Emission
sigma_Be=2.500*10**7 # omega**(-1)*m**(-1)
sigma_Al=3.538*10**7 # omega**(-1)*m**(-1)
sigma_Au=4.060*10**7 # omega**(-1)*m**(-1)
sigma_Ag=6.287*10**7 # omega**(-1)*m**(-1)
sigma = [sigma_Be, sigma_Al, sigma_Au, sigma_Ag]
epsilon=8.854187817620*10**(-12) #F/m


