import os
import librosa
import soundfile as sf
import random
from lib.components.datastructs.loop import Loop

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