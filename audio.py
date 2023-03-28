import librosa
import soundfile as sf

def stretch(loop, to_len):
    rate = len(loop.data)/to_len
    stretched = librosa.effects.time_stretch(y=loop.data, rate=rate)
    return stretched

def tune(loop, semitones_distance):
    tuned = librosa.effects.pitch_shift(y=loop.data, sr=48000, n_steps=semitones_distance)
    return tuned

def loadLoop(path, sr=48000):
    data, sr = librosa.load(path, sr=sr)
    return data, sr

def export(name = 'test.wav', audio=[], sr=48000):
    sf.write(name, audio, sr, 'PCM_16')