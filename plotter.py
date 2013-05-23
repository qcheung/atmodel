from numpy import log10
import matplotlib.pyplot as plt

def loglogplot(x, y):
    logx = log10(x)
    logy = log10(y)
    plt.plot(logx, logy)
    plt.show()
    
