# Applies naive fourier transform using actual piano frequencies, using a generated sin-wave audio spectrum.

import math
import random
from piano import PIANO_KEYS
from util import * 

sampling_rate = 2048        # samples per second.
key_threshold = 0.45         # threshold of a key to be recognized.

audio_duration = 1
key_strokes = 8
key_max_duration = (1, 8)
key_interval = 0.5

# test parameters
test_runs = 1

def generateSpectrum():
    spectrum = [0.0] * (sampling_rate * audio_duration)

    # selects the to-be-pressed pressed keys.
    key_count = int(random.random() * key_strokes + 1)
    pressed_keys = [[0] * 3] * key_count
    intervals = [0] * key_count

    # calculates some constants for the audio interval
    v = audio_duration / key_interval
    u = key_max_duration[1] / key_interval
    pi2 = math.pi * 2

    togglePrint("Generated Keys")
    for i in range(0, key_count): 
        # selects the pressed key.
        k = int(random.random() * len(PIANO_KEYS))

        # calculates its start and end time.
        s = math.floor(random.random() * v) * key_interval
        d = max(key_max_duration[0], math.floor(random.random() * u) * key_interval)
        e = min(s + d, audio_duration)

        # adds the keys stroke.
        key = PIANO_KEYS[k]
        pressed_keys[i] = key
        intervals[i] = (s, e)
        togglePrint(str(k) + " - " + str(PIANO_KEYS[k]) + " : " + str((s, e)))

        f = float(key[1]) / float(sampling_rate)
        l = 0; 
        rs = math.floor(s * sampling_rate)
        re = math.floor(e * sampling_rate)

        rs = 0
        re = sampling_rate * audio_duration

        for j in range(rs, re):
            m = math.sin(pi2 * l)
            l += f
            spectrum[j] += m
    
    return spectrum, pressed_keys, intervals


# generates a list of keys using an audio spectrum.
def spectrumToKeys(spectrum, ds, de):
    # the found keys container
    keys = []
    delta = de - ds

    # calculates the stepsize and the -2 * PI.
    neg2pi = math.pi * -2
    
    togglePrint("Found Keys:")
    # iterates through all possible piano keys.
    for j in range(0, len(PIANO_KEYS)):
        # selects  the current key, 
        # and calculates its function.
        key = PIANO_KEYS[j]
        f = float(key[1]) / sampling_rate

        # containers for complex number sums.
        r = 0
        i = 0

        # iterates through the spectrum.
        for t in range(ds, de): 
            # Applies inner FFT formula.
            g = spectrum[t]
            e = neg2pi * t * f
            r += g * math.cos(e)
            i += g * math.sin(e)

        # calulates the mean square root
        m = math.sqrt(r * r + i * i) / delta
        # print(m)

        # if m exceeds the threshold, 
        # it is considered played.
        if m > key_threshold * delta / sampling_rate: 
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
        spectrum, generated_keys, intervals = generateSpectrum()

        printArray(spectrum, "spectrum-out.csv")


        found_keys = spectrumToKeys(spectrum, 0, sampling_rate)
        error = calculateError(generated_keys, found_keys)
        average_error += error
    average_error /= test_runs
    print("Average Error: " + str(average_error))

if __name__ == "__main__": 
    main()
