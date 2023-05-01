import librosa
from lib.abstract import AudioComponent
import soundfile as sf
import numpy as np
import random
import os
from lib.util import DIVIDER

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
    
    def tune(self, tune):
        self.setData(tune(self, tune))

    def tone_stretch(self, bar_lenght):
        self.setData(tone_stretch(self, bar_lenght))

    def stretch(self, bar_lenght):
        self.setData(stretch(self, bar_lenght))

    def getId(self):
        return self.id
    
    def setTune(self, tune):
        self.tune = tune

    def getTune(self):
        return self.tune

    def getLen(self):
        return len(self.data)
    
    def getInfo(self):
        print(self.getName())

    def getRepr(self):
        return f'{self.getTune()}'
    
    def getHeir(self):
        return self

def check_min_len(loop, min_len, log=False):
    if log:
        print(f'| audio lenght: {len(loop.data)/loop.sr} sec')
    audio = loop.data
    sr = loop.sr
    ratio = min_len/len(audio)          
    if ratio > 1.6:                
        audio = np.append(audio, audio)
        if log:
            print(f'| Too short at loading, lenght after: {len(audio)/loop.sr}')
            print(f'-> Repeated {2} times, difference reduced by {(min_len/sr - (len(audio)/sr)/2)-(min_len/sr - len(audio)/sr)} sec\n')
        return np.array([audio])
    elif ratio < 0.5:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]
        if log:
            print(f'| Too long at loading, lenght after: {len(audio2_1)/loop.sr}') 
            print(f'-> Splitted in 2. Difference reduced by {(min_len/sr - (len(audio)/sr))-(len(audio2_1)/sr - min_len/sr)} sec\n')
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

def trim_loop(ref_len, data, log=False):
    audio = data.data
    ratio = ref_len / len(audio)
    if  ratio > 1.2:
        audio = np.repeat(audio, 2)
        if log:
            print(f'| Too short: {len(audio)/2*data.sr}. Ratio = {ratio} | Reference lenght: {ref_len/data.sr} sec')
            print(f'-> Audio doubled. Difference reduced by {(ref_len/data.sr - (len(audio)/data.sr)/2)-(ref_len/data.sr - len(audio)/data.sr)} sec')       
        return np.array([audio])
    elif ratio < 0.6:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]
        if log:
            print(f'| Too long: {len(audio)/data.sr}. Ratio = {ratio}')
            print(f'-> Divided in half. Difference reduced by {(ref_len/data.sr - midpoint*2/data.sr)-(ref_len/data.sr - midpoint/data.sr)} sec')
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