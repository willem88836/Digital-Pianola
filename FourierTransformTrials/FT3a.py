# Applies naive fourier transform using actual piano frequencies, using a generated sin-wave audio spectrum,
# and finds the interval during which the stroke is active.

import math
import random
from piano import PIANO_KEYS
from util import * 

sampling_rate = 1024        # samples per second.
key_threshold = 0.45         # threshold of a key to be recognized.

audio_duration = 16
key_strokes = 16
key_max_duration = (0.5, 8)
key_interval = 0.5

test_frame = 0.5        # in seconds
test_interval = 0.25    # in seconds


def generateSpectrum():
    spectrum = [0.0] * (sampling_rate * audio_duration)

    # selects the to-be-pressed pressed keys.
    key_count = int(random.random() * key_strokes + 1)
    pressed_keys = []
    intervals = []

    # calculates some constants for the audio interval
    v = audio_duration / key_interval
    u = key_max_duration[1] / key_interval
    pi2 = math.pi * 2

    for i in range(0, key_count): 
        # selects the pressed key.
        k = int(random.random() * len(PIANO_KEYS))
        key = PIANO_KEYS[k]

        # calculates its start and end time.
        s = math.floor(random.random() * v) * key_interval
        d = max(key_max_duration[0], math.floor(random.random() * u) * key_interval)
        e = min(s + d, audio_duration)

        # only adds unique keys 
        if (pressed_keys.__contains__(key)): 
            continue

        # adds the keys stroke.
        pressed_keys.append(key)
        intervals.append((s, e))

        f = float(key[1]) / float(sampling_rate)
        l = 0; 
        rs = math.floor(s * sampling_rate)
        re = math.floor(e * sampling_rate)

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

        # if m exceeds the threshold, 
        # it is considered played.
        if m > key_threshold * delta / sampling_rate: 
            keys.append(key)

    return keys

# Generates list of keys and when they start and end. 
def spectrumRangeToKeys(spectrum): 
    key_strokes = [] 

    # iterates through all audio frames.
    s = 0.0 
    while s < audio_duration - test_frame: 
        # selects the discrete start and endpoints
        e = s + test_frame
        ds = math.floor(s * sampling_rate)
        de = math.floor(e * sampling_rate)
        
        # generates keys on this interval
        keys = spectrumToKeys(spectrum, ds, de)

        # updates found keys if they persist along frames.
        for key in keys: 
            updated_key = False

            # backwards loop is faster.
            j = len(key_strokes) - 1
            while j >= 0: 
                listed = key_strokes[j]

                # if it's the same key, it might be updated.
                if listed[0] == key:
                    # the key is updated if the timeframes overlap.
                    if listed[1] <= s and listed[2] >= s: 
                        u = (key, listed[1], e)
                        key_strokes[j] = u
                        updated_key = True
                        break
                j -= 1

            # if no key was updated, the key is added. 
            if not updated_key:
                key_strokes.append((key, s, e))
                
        s += test_interval

    return key_strokes

def main(): 
    spectrum, generated_keys, intervals = generateSpectrum()

    print("Generated:")
    for i in range(0, len(generated_keys)):
        key = (generated_keys[i], intervals[i])
        print(key)

    found_keys = spectrumRangeToKeys(spectrum)
    
    print("Found:")
    for key in found_keys: 
        print(key)


if __name__ == "__main__": 
    main()
