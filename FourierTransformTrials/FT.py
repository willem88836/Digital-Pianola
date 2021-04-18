import math
import random

def printArray(a):
    for s in a: 
        print(str(s))

def generateSpectrum(): 
    n = 1024
    s = 1
    f = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    q = 0

    spectrum = [0] * n
    for i in range(0, n): 
        m = 0.0
        j = i * s
        for r in f: 
            m += math.sin(2 * math.pi * j * r) + (random.random() - 0.5) * q
        spectrum[i] = m
    return spectrum, f

def printResults(spectrum, frequency, sin_waves, k):
    i = 0
    f = []
    e = 0
    for j in range(1, len(frequency) - 1):
        if (frequency[j] > frequency[j - 1] and frequency[j] > frequency[j + 1] and frequency[j] > 0.4): 
            f.append(j * k)
            try:
                e += abs(j * k - sin_waves[i])
                i += 1
            except: 
                print("")
    e /= len(sin_waves)

    print("real: " + str(sin_waves))
    print("found: " + str(f))
    print("error: " + str(e))

    # printArray(spectrum)
    # print("")
    # printArray(frequency)


def fourierTransform(G, q, max):
    m = math.floor(max / q)
    ftf = [0.0] * m

    for s in range(1, m):
        f = q * s
        r = 0
        i = 0
        lg = len(G)
        for t in range(0, lg):
            g = G[t]
            e = -2 * math.pi * t * f
            r += g * math.cos(e)
            i += g * math.sin(e)
        ftf[s] = math.sqrt(r*r + i*i) / lg

    return ftf

def main(): 
    spectrum, sin_waves = generateSpectrum()

    k = 0.001
    l = 0.1
    frequency = fourierTransform(spectrum, k, l)

    printResults(spectrum, frequency, sin_waves, k)



if __name__ == "__main__": 
    main()