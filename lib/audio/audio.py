import librosa
from lib.components.abstract import AudioComponent
from lib.audio.loop import Loop
import soundfile as sf
import numpy as np
import random
import os

import logging
logger = logging.getLogger('my_logger')

def normalize(loop):
    data = loop.get_data()
    loop.set_data(data)
    return data

def trim_loop(loop, min_len):
    logger.debug(f'     Audio lenght: {len(loop.get_data())/loop.sr} sec')
    audio = loop.data
    sr = loop.sr
    ratio = min_len/len(audio)          
    if ratio > 1.3:
        array = audio                       
        audio = np.append(audio, array)
        logger.warning(f'Repeated {2} times, difference reduced by {(min_len/sr - (len(audio)/sr)/2)-(min_len/sr - len(audio)/sr)} sec')
        
        return np.array([audio])
    elif ratio < 0.7:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]
        logger.warning(f'Splitted in 2. Difference reduced by {(min_len/sr - (len(audio)/sr))-(len(audio2_1)/sr - min_len/sr)} sec')
        
        return [audio2_1, audio2_2]
    return np.array([audio])

def stretch_resample(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr
    stretch_ratio = to_len/cur_len
    stretched_audio = librosa.resample(y=audio, orig_sr=sr, target_sr=int(sr * stretch_ratio))
    if len(stretched_audio) < to_len:
        logger.warning(f'Padding {to_len - len(stretched_audio)} samples')
        padding_len = to_len - len(stretched_audio)
        stretched_audio = np.pad(stretched_audio, (0, padding_len), mode='constant')
    return stretched_audio[:to_len]

def stretch_key(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr  
    stretch_ratio = cur_len/to_len
    stretched_audio = librosa.effects.time_stretch(y=audio, rate=stretch_ratio)
    return stretched_audio

def tune(loop, semitones_distance):
    tuned = librosa.effects.pitch_shift(y=loop.data, sr=48000, n_steps=semitones_distance)
    return tuned

def loadLoop(path, sr):
    data, sr = librosa.load(path, sr=sr)
    return data, sr

def load_loop_from_path(path, sr):
    loop_name = random.choice(os.listdir(path))
    loop_path = os.path.join(path, loop_name)
    data, sr = loadLoop(loop_path, sr)           
    loop = Loop(id=0, name=loop_name, data=data, sr=sr, path=path)
    return loop

def export(name = 'test.wav', audio=[], sr=48000):
    sf.write(name, audio, sr, 'PCM_16')