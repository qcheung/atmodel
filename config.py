# atmodel: config.py
# configurable settings
# (including default input values)

SpecRes_Default = "1000"     # Spectral Resolution
MirrorDiam_Default = "2.2"  # Mirror Diameter (m)
MirrorTemp_Default = "2"  # Mirror Temperature (K)
StartFreq_Default = ".1"   # Starting Frequency (THz)
StopFreq_Default = "10"    # Ending Frequency (THz)
SigNoise_Default = "5"    # Signal to Noise Ratio
DependMin_Default = ""   # Dependent Minimum (10^x)
DependMax_Default = ""   # Dependent Maximum (10^x)

# what to calculate
Noise_Default = True    # total noise
Temp_Default = False     # total temperature
Signal_Default = False   # total signal
IntTime_Default = False  # integration time
