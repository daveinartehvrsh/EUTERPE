import os
import librosa
import soundfile as sf
import random
from lib.components.datastructs.loop import Loop
from lib.components.abstract.abstract import AudioComponent
import lib.utils.util as util
import logging
logger = logging.getLogger('my_logger')

def load(name, path, sr):
    data, sr = librosa.load(path, sr=sr)
    audio = AudioComponent(name=name, data=data, sr=sr, path=path)
    return audio

def rnd_loop(path, sr):
    options = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.wav'):
                options.append(os.path.join(root, file))
    logger.info(f'Found {len(options)} loops in {path}')
    loop_path = random.choice(options)
    loop_name = loop_path.split('\\')[-1]
    audio = load(name=loop_name, path=loop_path, sr=sr)
    bpm = util.extract_bpm_from_str(loop_name)
    scale = util.extract_scale_from_str(loop_name)           
    loop = Loop(id=0, name=loop_name, data=audio.get_data(), sr=sr, path=path, bpm=bpm, scale=scale)
    return loop

def export(name = 'test.wav', audio=[], sr=48000):
    sf.write(name, audio, sr, 'PCM_16')