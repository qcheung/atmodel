from numpy import log10
import matplotlib.pyplot as plt

def loglogplot(x, y):
    logx = log10(x)
    logy = log10(y)
    plt.plot(logx, logy)
    plt.xlabel("log(THz)")
    plt.ylabel("log()")
    plt.show()

#loglogplot([1,2,3,4,5,6],[10,20,30,40,60,80])
