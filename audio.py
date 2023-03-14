import librosa
from classes import *

def stretch():
    ...

def tune(loop, semitones_distance):
    tuned = librosa.effects.pitch_shift(y=loop.data, sr=48000, n_steps=semitones_distance)
    return tuned

def loadLoop(path, sr=48000):
    data, sr = librosa.load(path, sr=sr)
    loop = Loop(data=data, sr=sr, path=path)
    return loop

def export():
    ...

def render():
    ...