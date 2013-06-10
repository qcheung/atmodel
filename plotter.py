from numpy import log10
import matplotlib.pyplot as plt

def loglogplot(x, y):
    logx = log10(x)
    logy = log10(y)
    plt.plot(logx, logy)
<<<<<<< HEAD
    plt.xlabel('log(THz)')
    plt.ylabel('log()')
    plt.title('Histogram of IQ')
=======
    plt.xlabel("log(THz)")
    plt.ylabel("log()")
>>>>>>> f699e4b1b1fdc1a0187437ac5328b6fb04b54f0b
    plt.show()

#loglogplot([1,2,3,4,5,6],[10,20,30,40,60,80])
