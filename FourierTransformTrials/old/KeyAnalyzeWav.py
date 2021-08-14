
from joblib import Parallel, delayed 
import multiprocessing
import math
import librosa

from piano import PIANO_KEYS
from util import * 
import progress_bar as pb

# generates a list of keys using an audio spectrum.
def spectrum_to_keys(spectrum, start_index, end_index, sampling_rate, key_threshold) -> tuple[list[tuple], list[float]]:
    # the found keys container
    magnitudes = [0.0] * len(PIANO_KEYS)
    keys = []
    delta = end_index - start_index

    # calculates the stepsize and the -2 * PI.
    neg2pi = math.pi * -2
    
    # iterates through all possible piano keys.
    for j in range(0, len(PIANO_KEYS)):
        # selects  the current key, 
        # and calculates its function.
        key = PIANO_KEYS[j]
        func = float(key[1]) / sampling_rate

        # containers for complex number sums.
        re = 0
        im = 0

        # iterates through the spectrum.
        for t in range(start_index, end_index): 
            # Applies inner FFT formula.
            g = spectrum[t]
            e = neg2pi * t * func
            re += g * math.cos(e)
            im += g * math.sin(e)

        # calulates the mean square root
        mag = math.sqrt(re * re + im * im) / delta

        # if m exceeds the threshold, 
        # it is considered played.
        if mag > key_threshold * delta / sampling_rate: 
            keys.append(key)

        magnitudes[j] = mag
    
    return keys, magnitudes

def analyze_section(task_index, max_tasks, data_set, step_delta, data_frame_size, sampling_rate, key_threshold) -> list[tuple]: 
    keys = []
    try: 
        chunk_start = int(task_index * step_delta)
        chunk_end = chunk_start + data_frame_size
        data_chunk = data_set[chunk_start:chunk_end]
        keys, _ = spectrum_to_keys(data_chunk, 0, data_frame_size, sampling_rate, key_threshold)
    except: 
        print(f'Task {task_index} failed...')
    finally: 
        pb.update_progress(task_index, max_tasks)
        return keys    

def keystroke_analysis(filename) -> list[list[tuple]]:
    audio_data, sampling_rate = librosa.load(filename)
    duration_in_seconds = len(audio_data) / sampling_rate

    # loads beat interval
    beats_per_minute, _ = librosa.beat.beat_track(y=audio_data, sr=sampling_rate)
    beats_per_second = beats_per_minute / 60.0

    key_threshold = 0.005 
    step_delta = beats_per_second / 32 # assuming that 32 notes can be played rhythmically in one second.
    step_delta_sr = int(step_delta * sampling_rate)
    data_frame_size = 0.5
    data_frame_size_sr = int(data_frame_size * sampling_rate)
    step_count = int((duration_in_seconds / step_delta) - (data_frame_size / step_delta))
    # step_count = int(step_count * 0.03)
    cpu_cores = min(multiprocessing.cpu_count(), step_count)

    print(f'Started Key Stroke Analysis:\n\
        \tFile:\t\t\t{filename}\n\
        \tLength:\t\t\t{math.ceil(duration_in_seconds)} sec.\n\
        \tSampling Frequency:\t{sampling_rate} Hz.\n\
        \tRhythm:\t\t\t{beats_per_minute:.4f} BPM\n\
        \tStep Delta:\t\t{step_delta:.4f} sec. {step_delta_sr} samples\n\
        \tData Frame:\t\t{data_frame_size:.4f} sec. {data_frame_size_sr} samples\n\
        \tStep Count:\t\t{step_count} steps\n\
        \tKey Threshold:\t\t{key_threshold}\n\
        \tCPU Cores: \t\t{cpu_cores} cores')

    pb.update_progress(0, step_count)

    key_map = Parallel(n_jobs=cpu_cores)(delayed(analyze_section)(i, step_count, audio_data, step_delta_sr, data_frame_size_sr, sampling_rate, key_threshold) for i in range(0, step_count, 1))
    return key_map

file_path = relative_path('data\\Humdrum Days.wav')
key_map = keystroke_analysis(file_path)

file = open('data\\Humdrum Days.out', mode="w")
file.write(str(key_map))
