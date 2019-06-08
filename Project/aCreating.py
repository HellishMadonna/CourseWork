import sys
import random
from numpy.fft import fft
import math
import matplotlib.pyplot as plt
import configparser
import os

def getStr(_list):
    st = ""
    for i in range(len(_list) - 1):
        st += str(_list[i]) + "; "

    st += str(_list[len(_list)-1])
    return st

def main(argv = None):
    if (argv is None):
        argv = sys.argv

    config = configparser.ConfigParser()
    f = open("input.txt", "w")

    a = []
    maxI = 1024

    x = []
    for q in range(maxI):
        x.append(q * math.pi / maxI)
    
    step = 1 / 200

    cur = 0.9
    for i in range(maxI):
        f.write(str(cur))
        if (i + 1 < maxI):
            f.write(" ")
            
        a.append(cur)
        if (i < 600):
            cur = cur    
        elif (i < 700):
            cur -= step

    #print(a)

    #print(getStr(a))
    config.add_section("Settings")
    config.set("Settings", "Amplitude-Frequency", getStr(a))
   
    config.set("Settings", "SpeciesCount", "100")
    config.set("Settings", "IterationsCount", "50")
    config.set("Settings", "MaxCoefCount", "10")
    config.set("Settings", "Epsilon", "0.01")

    config.write(open("input.ini", "w"))

    
    plt.plot(x, a)
    plt.savefig('test.png', format = 'png')
    
if __name__ == "__main__":
    sys.exit(main())
