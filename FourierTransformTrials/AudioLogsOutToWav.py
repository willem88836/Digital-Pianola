
from util import relative_path
from piano import PIANO_KEYS
import math
import soundfile
from util import * 

file = open('data\\Humdrum Days.out'); 
data = file.read()
split = data.split('],')

count = 0
seq = ""
seqs = []
for entry in split: 
    if entry.startswith(' [[') or entry == ' [': 
        count += 1 
        seqs.append(seq)
        seq = ""
    else: 
        seq = seq + entry
    
q = 0.0
r = 0.0421
key_strokes = []
for entry in seqs: 
    cleaned = entry.strip(" []")
    keys = cleaned.split('[')
    taps = [0] * len(keys)
    o = 0
    for key in keys: 
        name = key.split(',')[0].strip("'")
        for i in range(0, len(PIANO_KEYS)): 
            if (name == PIANO_KEYS[i][0]): 
                taps[o] = i
                o += 1
                break
    key_strokes.append([q, taps])
    q += r

pi2 = math.pi * 2
sampling_rate = 22050
spectrum = [0.0] * math.ceil(q * sampling_rate)

for i in range(0, len(key_strokes)): 
    entry = key_strokes[i]
    time = entry[0]
    keys = entry[1]
    t = i * r
    q = r / sampling_rate
    p = int(sampling_rate * r) 

    for key in keys: 
        f = PIANO_KEYS[key][1] / float(sampling_rate)
        k = i * p
        l = k * f
        for j in range(0, p): 
            m = math.sin(pi2 * l)
            spectrum[k + j] += m
            l += f
print(spectrum)
soundfile.write(relative_path('data\\generated_audio.wav'), spectrum, sampling_rate)
