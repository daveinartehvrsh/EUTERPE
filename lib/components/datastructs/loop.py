from lib.components.abstract.abstract import AudioComponent
import lib.audio as audio

import logging
logger = logging.getLogger('my_logger')

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str, bpm: int = None, st_shift: int = 0, scale: int = None):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
        self.st_shift = st_shift
        self.scale = scale
        self.gain = 1
        self.bpm = bpm
    
    def trim(self, lenght):
        loops = audio.transform.trim_loop(self, lenght)
        self.set_data(loops[0])
        if len(loops) > 1:
            return loops
        return None

    def tune(self, st_shift):
        self.set_data(audio.tune.st_shift(self, st_shift))
        self.st_shift += st_shift

    def stretch(self, bar_lenght, mode='key'):
        logger.debug(f'Stretching {self.get_name()} from {float("{:.2f}".format(self.get_len()/self.sr))}s to {float("{:.2f}".format(bar_lenght/self.sr))}s with {mode} mode')
        if mode == 'key':
            self.set_data(audio.stretch.stretch_key(self, bar_lenght))
        elif mode == 'resample':
            self.set_data(audio.stretch.stretch_resample(self, bar_lenght))
    
    def set_scale(self, scale):
        self.scale = scale

    def get_scale(self):
        return self.scale

    def get_id(self):
        return self.id

    def get_tune(self):
        return self.st_shift

    def get_path(self):
        return self.path

    def get_repr(self):
        return f'{self.get_tune()}'

    def get_bpm(self):
        return self.bpm
        
    def get_info(self):
        info = {
            'id': self.get_id(),
            'name': self.name,
            'data': self.data,
            'sr': self.sr,
            'path': self.get_path(),
            'scale': self.scale,
            'st_shift': self.get_tune(),
            'gain': self.get_gain()
        }

class Track(Loop):
    ...