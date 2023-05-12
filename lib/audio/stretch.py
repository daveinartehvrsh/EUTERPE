import librosa
from lib.components.abstract.abstract import AudioComponent
import numpy as np
import logging
logger = logging.getLogger('my_logger')

def stretch_resample(loop, to_len):
    audio = loop.data
    cur_len = len(audio)
    sr = loop.sr
    stretch_ratio = to_len/cur_len
    stretched_audio = librosa.resample(y=audio, orig_sr=sr, target_sr=int(sr * stretch_ratio))
    if len(stretched_audio) < to_len:
        logger.warning(f'WARN: Padding {to_len - len(stretched_audio)} samples')
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
