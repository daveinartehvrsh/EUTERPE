import numpy as np
from lib.components.abstract.abstract import AudioComponent
import librosa
import logging
logger = logging.getLogger('my_logger')

def normalize(audio: AudioComponent):
    data = audio.get_data()
    audio.set_data(librosa.util.normalize(data))
    return data

def trim_loop(audio: AudioComponent, min_len):
    logger.debug(f'audio lenght: {len(audio.get_data())/audio.sr} sec')
    sr = audio.sr
    audio = audio.data
    
    ratio = min_len/len(audio)          
    if ratio > 1.3:
        array = audio                       
        audio = np.append(audio, array)
        logger.warning(f'WARN: Repeated {2} times, difference reduced by {(min_len/sr - (len(audio)/sr)/2)-(min_len/sr - len(audio)/sr)} sec')
        
        return np.array([audio])
    elif ratio < 0.7:
        midpoint = int((len(audio) / 2) + 0.5) 
        audio2_1 = audio[:midpoint]
        audio2_2 = audio[midpoint:]
        logger.warning(f'WARN: Splitted in 2. Difference reduced by {(min_len/sr - (len(audio)/sr))-(len(audio2_1)/sr - min_len/sr)} sec')
        
        return [audio2_1, audio2_2]
    return np.array([audio])
