import librosa
from lib.components.abstract import AudioComponent
import soundfile as sf
import numpy as np
import random
import os

import logging
logger = logging.getLogger('my_logger')

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str, tune_st: int = 0):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
        self.tune_st = tune_st
    
    def tune(self, tune_st):
        self.set_data(tune(self, tune_st))
        self.tune_st += tune_st

    def tone_stretch(self, bar_lenght):
        self.set_data(tone_stretch(self, bar_lenght))

    def stretch(self, bar_lenght):
        self.set_data(stretch(self, bar_lenght))

    def get_sr(self):
        return self.sr

    def get_id(self):
        return self.id

    def get_tune(self):
        return self.tune_st

    def get_len(self):
        return len(self.data)
    
    def get_path(self):
        return self.path

    def get_info(self):
        info = {
            'id': self.get_id(),
            'name': self.name,
            'data': self.data,
            'sr': self.sr,
            'path': self.get_path(),
            'tune': self.get_tune()
        }

    def get_repr(self):
        return f'{self.get_tune()}'
    
    def get_heir(self):
        return self

def check_min_len(loop, min_len):

    logger.debug(f'Audio lenght: {len(loop.get_data())/loop.sr} sec')

    audio = loop.data
    sr = loop.sr
    ratio = min_len/len(audio)          
    if ratio > 1.4:                        
        audio = np.append(audio, audio)

        logger.info(f'Too short at loading, lenght after: {len(audio)/loop.sr}')
        logger.warning(f'Repeated {2} times, difference reduced by {(min_len/sr - (len(audio)/sr)/2)-(min_len/sr - len(audio)/sr)} sec')
        
        return np.array([audio])
    elif ratio < 0.7:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]

        logger.info(f'Too long at loading, lenght after: {len(audio2_1)/loop.sr}') 
        logger.warning(f'Splitted in 2. Difference reduced by {(min_len/sr - (len(audio)/sr))-(len(audio2_1)/sr - min_len/sr)} sec')
        
        return [audio2_1, audio2_2]
    return np.array([audio])

def stretch(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr
    stretch_ratio = to_len/cur_len
    stretched_audio = librosa.resample(y=audio, orig_sr=sr, target_sr=int(sr * stretch_ratio))
    if len(stretched_audio) < to_len:
        padding_len = to_len - len(stretched_audio)
        stretched_audio = np.pad(stretched_audio, (0, padding_len), mode='constant')
    return stretched_audio[:to_len]

def tone_stretch(loop, to_len):
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

def trim_loop(ref_len, data):
    audio = data.data
    ratio = ref_len / len(audio)
    if  ratio > 1.2:
        audio = np.repeat(audio, 2)

        logger.info(f'Too short: {len(audio)/2*data.sr}. Ratio = {ratio} | Reference lenght: {ref_len/data.sr} sec')
        logger.warning(f'Audio doubled. Difference reduced by {(ref_len/data.sr - (len(audio)/data.sr)/2)-(ref_len/data.sr - len(audio)/data.sr)} sec')       

        return np.array([audio])
    elif ratio < 0.6:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]

        logger.info(f'Too long: {len(audio)/data.sr}. Ratio = {ratio}')
        logger.warning(f'Divided in half. Difference reduced by {(ref_len/data.sr - midpoint*2/data.sr)-(ref_len/data.sr - midpoint/data.sr)} sec')

        return [audio2_1, audio2_2]
    else:    
        return None

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