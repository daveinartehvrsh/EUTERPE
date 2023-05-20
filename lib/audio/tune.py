import librosa
from lib.components.abstract.abstract import AudioComponent

def st_shift(audio: AudioComponent, semitones_distance: int):
    tuned = librosa.effects.pitch_shift(y=audio.data, sr=48000, n_steps=semitones_distance)
    return tuned
