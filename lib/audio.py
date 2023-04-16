import librosa
import soundfile as sf
import numpy as np

def stretch(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr
    stretch_ratio = to_len / cur_len
    #new_len = int(cur_len * stretch_ratio)
    stretched_audio = librosa.resample(y=audio, orig_sr=sr, target_sr=int(sr * stretch_ratio))
    if len(stretched_audio) < to_len:
        padding_len = to_len - len(stretched_audio)
        stretched_audio = np.pad(stretched_audio, (0, padding_len), mode='constant')
    return stretched_audio[:to_len]

def tune(loop, semitones_distance):
    tuned = librosa.effects.pitch_shift(y=loop.data, sr=48000, n_steps=semitones_distance)
    return tuned

def loadLoop(path, sr=48000):
    data, sr = librosa.load(path, sr=sr)
    return data, sr

def get_tonality(loop):
    y = loop.data
    sr = loop.sr
    pitch = librosa.core.pitch.estimate_tuning(y=y, sr=sr)
    return pitch


def check_audio_length(ref_len, audio2):
    if len(audio2) < ref_len / 2:
        audio2 = audio2 * 2
    elif len(audio2) > ref_len * 2:
        midpoint = len(audio2) // 2
        audio2_1 = audio2[:midpoint]
        audio2_2 = audio2[midpoint:]
        return [audio2_1, audio2_2], 2
    return [audio2], 1

def export(name = 'test.wav', audio=[], sr=48000):
    sf.write(name, audio, sr, 'PCM_16')


def main():
    ...
    
if __name__ == "__main__":
    main()