import librosa
from lib.components.abstract import AudioComponent
import soundfile as sf
import numpy as np
import random
import os

import logging
logger = logging.getLogger('my_logger')

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str, st_shift: int = 0, scale: int = None):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
        self.st_shift = st_shift
        self.scale = scale
        self.gain = 1
    
    def trim(self, lenght):
        loops = trim_loop(self, lenght)
        self.set_data(loops[0])
        if len(loops) > 1:
            return loops
        return None

    def tune(self, st_shift):
        self.set_data(tune(self, st_shift))
        self.st_shift += st_shift

    def stretch(self, bar_lenght, mode='key'):
        if mode == 'key':
            self.set_data(stretch_key(self, bar_lenght))
        elif mode == 'resample':
            self.set_data(stretch_resample(self, bar_lenght))

    def normalize(self):
        self.set_data(normalize(self))

    def set_scale(self, scale):
        self.scale = scale

    def get_scale(self):
        return self.scale

    def set_gain(self, gain):
        self.gain = gain

    def get_gain(self):
        return self.gain

    def get_sr(self):
        return self.sr

    def get_id(self):
        return self.id

    def get_tune(self):
        return self.st_shift

    def get_path(self):
        return self.path

    def get_repr(self):
        return f'{self.get_tune()}'
    
    def get_heir(self):
        return self
    
    def get_info(self):
        info = {
            'id': self.get_id(),
            'name': self.name,
            'data': self.data,
            'sr': self.sr,
            'path': self.get_path(),
            'scale': self.scale,
            'st_shift': self.get_tune(),
            'gain': self.get_gain()
        }

def normalize(loop):
    data = loop.get_data()
    loop.set_data(data)
    return data

def trim_loop(loop, min_len):

    logger.debug(f'Audio lenght: {len(loop.get_data())/loop.sr} sec')

    audio = loop.data
    sr = loop.sr
    ratio = min_len/len(audio)          
    if ratio > 1.7:
        array = audio                       
        audio = np.append(audio, array)

        logger.info(f'Too short at loading, lenght after: {len(audio)/loop.sr}')
        logger.warning(f'Repeated {2} times, difference reduced by {(min_len/sr - (len(audio)/sr)/2)-(min_len/sr - len(audio)/sr)} sec')
        
        return np.array([audio])
    elif ratio < 0.5:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]

        logger.info(f'Too long at loading, lenght after: {len(audio2_1)/loop.sr}') 
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
        padding_len = to_len - len(stretched_audio)
        stretched_audio = np.pad(stretched_audio, (0, padding_len), mode='constant')
    return stretched_audio[:to_len]

def stretch_key(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr  
    stretch_ratio = to_len/cur_len
    stretched_audio = librosa.effects.time_stretch(y=audio, rate=stretch_ratio)
    if len(stretched_audio) < to_len:
        padding_len = to_len - len(stretched_audio)
        stretched_audio = np.pad(stretched_audio, (0, padding_len), mode='constant')
    return stretched_audio[:to_len]

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

#NOT WORKING PROPERLY
def estimate_tuning(loop):
    y = loop.data
    sr = loop.sr
    pitch = librosa.core.pitch.estimate_tuning(y=y, sr=sr)
    return pitch


def main():
    ...   
if __name__ == "__main__":
    main()