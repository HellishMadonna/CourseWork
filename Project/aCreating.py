import sys
import random
from numpy.fft import fft
import math
import matplotlib.pyplot as plt

def main(argv = None):
    if (argv is None):
        argv = sys.argv

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

    plt.plot(x, a)
    plt.savefig('test.png', format = 'png')
    
if __name__ == "__main__":
    sys.exit(main())
