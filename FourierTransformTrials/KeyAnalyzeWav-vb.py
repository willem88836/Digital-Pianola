
from joblib import Parallel, delayed 
import multiprocessing
import math
import librosa
import soundfile
from functools import cmp_to_key

from piano import PIANO_KEYS
from util import * 
import progress_bar as pb

progress = None

class analysis_settings: 
    def __init__(self, seconds, key_threshold, test_interval, data_frame_size, max_processors) -> None:
        self.seconds = seconds
        self.key_threshold = key_threshold
        self.test_interval = test_interval
        self.data_frame_size = data_frame_size
        self.max_processors = max_processors

# generates a list of keys using an audio spectrum.
def spectrum_to_keys(spectrum:list[float], frame_size:int, sampling_rate:int, key_threshold:float) -> list[tuple]:
    # the found keys container
    keys = []

    key_threshold = key_threshold / sampling_rate

    # calculates the stepsize and the -2 * PI.
    neg2pi = math.pi * -2.0
    
    # iterates through all possible piano keys.
    for j in range(0, len(PIANO_KEYS)):
        # selects  the current key, 
        # and calculates its function.
        key = PIANO_KEYS[j]
        func = float(key[1]) / sampling_rate

        # containers for complex number sums.
        re = 0.0
        im = 0.0

        # iterates through the spectrum.
        for t in range(0, frame_size): 
            # Applies inner FFT formula.
            g = spectrum[t]
            e = neg2pi * t * func
            re += g * math.cos(e)
            im += g * math.sin(e)

        # calulates the mean square root
        mag = math.sqrt(re * re + im * im) / frame_size

        # if m exceeds the threshold, 
        # it is considered played.
        if mag > key_threshold:
            keys.append([j, mag])

    return keys

def analyze_section(task_index:int, progress:pb.progress_bar, data_set:list[float], step_delta:int, data_frame_size:float, sampling_rate:int, key_threshold:float) -> list[tuple]: 
    keys = None
    try: 
        chunk_start = int(task_index * step_delta)
        chunk_end = chunk_start + data_frame_size
        data_chunk = data_set[chunk_start:chunk_end]
        keys = spectrum_to_keys(data_chunk, data_frame_size, sampling_rate, key_threshold)
    except: 
        keys = []
        print(f'Task {task_index} failed...')
    finally: 
        progress.update_progress(task_index)
        return keys    

def keystroke_analysis(filename:str, settings:analysis_settings) -> list[list[tuple]]:
    audio_data, sampling_rate = librosa.load(filename)
    duration_in_seconds = len(audio_data) / sampling_rate
    duration_in_seconds = min(duration_in_seconds, settings.seconds)

    # loads beat interval
    beats_per_minute, _ = librosa.beat.beat_track(y=audio_data, sr=sampling_rate)
    beats_per_second = beats_per_minute / 60.0

    key_threshold = settings.key_threshold * sampling_rate
    step_delta = beats_per_second / settings.test_interval # assuming that 32 notes can be played rhythmically in one second.
    step_delta_sr = int(step_delta * sampling_rate)
    data_frame_size = settings.data_frame_size
    data_frame_size_sr = int(data_frame_size * sampling_rate)
    step_count = int((duration_in_seconds / step_delta) - (data_frame_size / step_delta))
    cpu_cores = min(multiprocessing.cpu_count(), settings.max_processors, step_count)
    
    header = f'Key Stroke Analysis:\n\
        File:\t\t\t{filename}\n\
        Length:\t\t\t{duration_in_seconds:.4f} sec.\n\
        Sampling Frequency:\t{sampling_rate} Hz.\n\
        Rhythm:\t\t\t{beats_per_minute:.4f} BPM\n\
        Step Delta:\t\t{step_delta:.4f} sec. {step_delta_sr} samples\n\
        Data Frame:\t\t{data_frame_size:.4f} sec. {data_frame_size_sr} samples\n\
        Step Count:\t\t{step_count} steps\n\
        Key Threshold:\t\t{key_threshold}\n\
        CPU Cores: \t\t{cpu_cores} cores'
    print(header)

    progress = pb.progress_bar(step_count + 1, 50)
    
    key_map = Parallel(n_jobs=cpu_cores)(delayed(analyze_section)(i, progress, audio_data, step_delta_sr, data_frame_size_sr, sampling_rate, key_threshold) for i in range(0, step_count, 1))
    condensed = condense_keystrokes(key_map, step_delta)

    progress.update_progress(step_count + 1)

    return condensed, key_map, header, duration_in_seconds

def condense_keystrokes(key_map:list[tuple], measure_interval:float) -> list[tuple]: 
    recorded_strokes = []
    current_time = 0.0
    active_keys = dict()
    passed_keys = set()

    for keys in key_map: 
        for key in keys: 
            key_index = key[0]
            key_magnitude = key[1] # TODO: use the derivative to figure out whether the key is pressed anew.

            if not active_keys.__contains__(key_index): 
                active_keys[key_index] = current_time

            passed_keys.add(key_index)

        released_keys = []
        for key in active_keys: 
            if not passed_keys.__contains__(key): 
                released_keys.append(key)
        
        for l in released_keys: 
            recorded_strokes.append([l, active_keys[l], current_time])
            del active_keys[l]

        passed_keys.clear()
        current_time += measure_interval

    return recorded_strokes

def stroke_data_to_wav(key_strokes:list[tuple], length_in_seconds:int, sampling_rate:int) -> list[float]: 
    sorted(key_strokes, key=cmp_to_key(lambda A, B: A[0] - B[0]))
    audio = [0.0] * (length_in_seconds * sampling_rate)
    
    pi2 = math.pi * 2

    for key in key_strokes: 
        key_frequency = PIANO_KEYS[key[0]][1] / sampling_rate
        l = key[1]
        key_start = int(l * sampling_rate)
        key_end = int(key[2] * sampling_rate)

        for i in range(key_start, key_end): 
            audio[i] += math.sin(pi2 * l)
            l += key_frequency

    return audio

file_name = 'data\\Humdrum Days'
file_path = relative_path(f'{file_name}.wav')
settings = analysis_settings(6, 0.006, 32, 0.5, 7)
condensed, key_map, header, duration_in_seconds = keystroke_analysis(file_path, settings)

open(f'{file_name}.out', mode="w").write(f'{header}\n\n{condensed}')

sampling_rate = 22050
generated_audio = stroke_data_to_wav(condensed, duration_in_seconds, sampling_rate)
soundfile.write(f'{relative_path(file_name)} (generated).wav', generated_audio, sampling_rate)
