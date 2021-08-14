
from joblib import Parallel, delayed 
import multiprocessing
import math
import librosa

from piano import PIANO_KEYS
from util import * 
import progress_bar as pb

class analysis_settings: 
    def __init__(self, seconds, key_threshold, test_interval, data_frame_size, max_processors) -> None:
        self.seconds = seconds
        self.key_threshold = key_threshold
        self.test_interval = test_interval
        self.data_frame_size = data_frame_size
        self.max_processors = max_processors

# generates a list of keys using an audio spectrum.
def spectrum_to_keys(spectrum, frame_size, sampling_rate, key_threshold) -> tuple[list[tuple], list[float]]:
    # the found keys container
    key_magnitudes = []
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
            keys.append(key)
            key_magnitudes.append(mag)

    return keys, key_magnitudes

def analyze_section(task_index, max_tasks, data_set, step_delta, data_frame_size, sampling_rate, key_threshold) -> list[tuple]: 
    keys = None
    try: 
        chunk_start = int(task_index * step_delta)
        chunk_end = chunk_start + data_frame_size
        data_chunk = data_set[chunk_start:chunk_end]
        keys, key_magnitudes = spectrum_to_keys(data_chunk, data_frame_size, sampling_rate, key_threshold)
    except: 
        keys = []
        print(f'Task {task_index} failed...')
    finally: 
        pb.update_progress(task_index, max_tasks)
        return keys    

def keystroke_analysis(filename: str, settings: analysis_settings) -> list[list[tuple]]:
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
        \tFile:\t\t\t{filename}\n\
        \tLength:\t\t\t{duration_in_seconds:.4f} sec.\n\
        \tSampling Frequency:\t{sampling_rate} Hz.\n\
        \tRhythm:\t\t\t{beats_per_minute:.4f} BPM\n\
        \tStep Delta:\t\t{step_delta:.4f} sec. {step_delta_sr} samples\n\
        \tData Frame:\t\t{data_frame_size:.4f} sec. {data_frame_size_sr} samples\n\
        \tStep Count:\t\t{step_count} steps\n\
        \tKey Threshold:\t\t{key_threshold}\n\
        \tCPU Cores: \t\t{cpu_cores} cores'
    print(header)

    pb.update_progress(0, step_count)

    key_map = Parallel(n_jobs=cpu_cores)(delayed(analyze_section)(i, step_count, audio_data, step_delta_sr, data_frame_size_sr, sampling_rate, key_threshold) for i in range(0, step_count, 1))

    pb.update_progress(step_count, step_count)

    return key_map, header

file_name = 'data\\Humdrum Days'
file_path = relative_path(f'{file_name}.wav')
settings = analysis_settings(4, 0.015, 32, 0.5, 7)
key_map, header = keystroke_analysis(file_path, settings)
open(f'{file_name}.out', mode="w").write(str(key_map))
