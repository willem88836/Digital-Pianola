# Applies naive fourier transform using actual piano frequencies, using a generated sin-wave audio spectrum.


import math
import random

PIANO_KEYS = [
    # key, frequency(Hz), Wavelength (cm)
    ['C#0/Db0', 17.32, 1991.47], 
    ['D0', 18.35, 1879.69], 
    ['D#0/Eb0', 19.45, 1774.2], 
    ['E0', 20.6, 1674.62], 
    ['F0', 21.83, 1580.63], 
    ['F#0/Gb0', 23.12, 1491.91], 
    ['G0', 24.5, 1408.18], 
    ['G#0/Ab0', 25.96, 1329.14], 
    ['A0', 27.5, 1254.55], 
    ['A#0/Bb0', 29.14, 1184.13],
    ['B0', 30.87, 1117.67], 
    ['C1', 32.7, 1054.94], 
    ['C#1/Db1', 34.65, 995.73], 
    ['D1', 36.71, 939.85], 
    ['D#1/Eb1', 38.89, 887.1], 
    ['E1', 41.2, 837.31], 
    ['F1', 43.65, 790.31], 
    ['F#1/Gb1', 46.25, 745.96], 
    ['G1', 49.0, 704.09], 
    ['G#1/Ab1', 51.91, 664.57], 
    ['A1', 55.0, 627.27], 
    ['A#1/Bb1', 58.27, 592.07], 
    ['B1', 61.74, 558.84], 
    ['C2', 65.41, 527.47], 
    ['C#2/Db2', 69.3, 497.87], 
    ['D2', 73.42, 469.92], 
    ['D#2/Eb2', 77.78, 443.55], 
    ['E2', 82.41, 418.65], 
    ['F2', 87.31, 395.16], 
    ['F#2/Gb2', 92.5, 372.98], 
    ['G2', 98.0, 352.04], 
    ['G#2/Ab2', 103.83, 332.29], 
    ['A2', 110.0, 313.64], 
    ['A#2/Bb2', 116.54, 296.03], 
    ['B2', 123.47, 279.42], 
    ['C3', 130.81, 263.74], 
    ['C#3/Db3', 138.59, 248.93], 
    ['D3', 146.83, 234.96], 
    ['D#3/Eb3', 155.56, 221.77], 
    ['E3', 164.81, 209.33], 
    ['F3', 174.61, 197.58], 
    ['F#3/Gb3', 185.0, 186.49],
    ['G3', 196.0, 176.02], 
    ['G#3/Ab3', 207.65, 166.14], 
    ['A3', 220.0, 156.82], 
    ['A#3/Bb3', 233.08, 148.02], 
    ['B3', 246.94, 139.71], 
    ['C4', 261.63, 131.87], 
    ['C#4/Db4', 277.18, 124.47], 
    ['D4', 293.66, 117.48], 
    ['D#4/Eb4', 311.13, 110.89], 
    ['E4', 329.63, 104.66], 
    ['F4', 349.23, 98.79], 
    ['F#4/Gb4', 369.99, 93.24], 
    ['G4', 392.0, 88.01], 
    ['G#4/Ab4', 415.3, 83.07], 
    ['A4', 440.0, 78.41], 
    ['A#4/Bb4', 466.16, 74.01], 
    ['B4', 493.88, 69.85], 
    ['C5', 523.25, 65.93], 
    ['C#5/Db5', 554.37, 62.23], 
    ['D5', 587.33, 58.74], 
    ['D#5/Eb5', 622.25, 55.44], 
    ['E5', 659.25, 52.33], 
    ['F5', 698.46, 49.39], 
    ['F#5/Gb5', 739.99, 46.62], 
    ['G5', 783.99, 44.01], 
    ['G#5/Ab5', 830.61, 41.54], 
    ['A5', 880.0, 39.2], 
    ['A#5/Bb5', 932.33, 37.0], 
    ['B5', 987.77, 34.93],
    ['C6', 1046.5, 32.97], 
    ['C#6/Db6', 1108.73, 31.12], 
    ['D6', 1174.66, 29.37], 
    ['D#6/Eb6', 1244.51, 27.72], 
    ['E6', 1318.51, 26.17], 
    ['F6', 1396.91, 24.7], 
    ['F#6/Gb6', 1479.98, 23.31], 
    ['G6', 1567.98, 22.0], 
    ['G#6/Ab6', 1661.22, 20.77], 
    ['A6', 1760.0, 19.6], 
    ['A#6/Bb6', 1864.66, 18.5], 
    ['B6', 1975.53, 17.46], 
    ['C7', 2093.0, 16.48], 
    ['C#7/Db7', 2217.46, 15.56], 
    ['D7', 2349.32, 14.69], 
    ['D#7/Eb7', 2489.02, 13.86], 
    ['E7', 2637.02, 13.08], 
    ['F7', 2793.83, 12.35], 
    ['F#7/Gb7', 2959.96, 11.66], 
    ['G7', 3135.96, 11.0], 
    ['G#7/Ab7', 3322.44, 10.38],
    ['A7', 3520.0, 9.8], 
    ['A#7/Bb7', 3729.31, 9.25],
    ['B7', 3951.07, 8.73], 
    ['C8', 4186.01, 8.24], 
    ['C#8/Db8', 4434.92, 7.78], 
    ['D8', 4698.63, 7.34], 
    ['D#8/Eb8', 4978.03, 6.93], 
    ['E8', 5274.04, 6.54], 
    ['F8', 5587.65, 6.17], 
    ['F#8/Gb8', 5919.91, 5.83], 
    ['G8', 6271.93, 5.5], 
    ['G#8/Ab8', 6644.88, 5.19], 
    ['A8', 7040.0, 4.9], 
    ['A#8/Bb8', 7458.62, 4.63], 
    ['B8', 7902.13, 4.37]
] 

sampling_size = 1024        # samples per second.
sample_duration = 1        # duration of the sample in seconds.
max_keys = 8                # maximum number of keys played simultaneously.
key_threshold = 0.45         # threshold of a key to be recognized.

# test parameters
test_runs = 1
should_print = True

def togglePrint(message):
    if should_print: 
        print(message)


# generates a audio spectrum using a random 
# set of piano keys.
def generateSpectrum():
    n = math.floor(sampling_size * sample_duration)
    spectrum = [0] * n

    # number of simulated keys.
    key_count = math.floor(random.random() * max_keys + 1)
    keys = [[] * 3] * key_count

    togglePrint("Generated keys:")
    for i in range(0, key_count):
        # selects a random key.
        k = math.floor(random.random() * len(PIANO_KEYS))
        key = PIANO_KEYS[k]

        if keys.__contains__(key): 
            i -= 1
            continue

        # calculates its function.
        f = float(key[1]) / sampling_size
        l = 0; 

        # logging + return values.
        togglePrint(str(k) + ": " + str(key))
        keys[i] = key

        # generates values for this key.
        for j in range(0, n): 
            m = math.sin(2 * math.pi * l)
            l += f
            spectrum[j] += m
            
    return spectrum, keys


# generates a list of keys using an audio spectrum.
def spectrumToKeys(spectrum):
    # the found keys container
    keys = []

    # calculates the stepsize and the -2 * PI.
    neg2pi = math.pi * -2
    
    togglePrint("Found Keys:")
    # iterates through all possible piano keys.
    for j in range(0, len(PIANO_KEYS)):
        # selects  the current key, 
        # and calculates its function.
        key = PIANO_KEYS[j]
        f = float(key[1]) / sampling_size

        # containers for complex number sums.
        r = 0
        i = 0

        # iterates through the spectrum.
        for t in range(0, len(spectrum)): 
            # Applies inner FFT formula.
            g = spectrum[t]
            e = neg2pi * t * f
            r += g * math.cos(e)
            i += g * math.sin(e)

        # calulates the mean square root
        m = math.sqrt(r * r + i * i) / sampling_size
        
        # if m exceeds the threshold, 
        # it is considered played.
        if m > key_threshold * sample_duration: 
            keys.append(key)
            togglePrint(str(j) + ": " + str(key))

    return keys

def calculateError(generated, found):
    error = 0.0

    for key in generated: 
        if not found.__contains__(key): 
            error += 1

    for key in found: 
        if not generated.__contains__(key): 
            error += 1

    error /= len(generated)

    togglePrint("Error: " + str(error))
    return error


def main(): 
    average_error = 0
    for i in range(0, test_runs): 
        print(str(i + 1) + "/" + str(test_runs))
        spectrum, generated_keys = generateSpectrum()
        found_keys = spectrumToKeys(spectrum)
        error = calculateError(generated_keys, found_keys)
        average_error += error
    average_error /= test_runs
    print("Average Error: " + str(average_error))



if __name__ == "__main__": 
    main()
