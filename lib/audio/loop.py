from lib.components.abstract import AudioComponent
import lib.audio.audio as audio

import logging
logger = logging.getLogger('my_logger')

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str, st_shift: int = 0, scale: int = None):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
        self.st_shift = st_shift
        self.scale = scale
        self.gain = 1
    
    def trim(self, lenght):
        loops = audio.trim_loop(self, lenght)
        self.set_data(loops[0])
        if len(loops) > 1:
            return loops
        return None

    def tune(self, st_shift):
        self.set_data(audio.tune(self, st_shift))
        self.st_shift += st_shift

    def stretch(self, bar_lenght, mode='key'):
        logger.info(f'      Stretching {self.get_name()} from {self.get_len()} to {bar_lenght} bars with {mode} mode')
        if mode == 'key':
            self.set_data(audio.stretch_key(self, bar_lenght))
        elif mode == 'resample':
            self.set_data(audio.stretch_resample(self, bar_lenght))

    def normalize(self, gain=None):
        if gain is not None:
            self.set_gain_db(gain)
            self.set_data(audio.normalize(self)*self.get_gain())
            logger.info(f'      Normalized {self.get_name()} to -{self.get_gain()} dB')
        else:    
            self.set_data(audio.normalize(self))
            logger.info(f'      Normalized {self.get_name()} to 0 dB')
        
    def set_scale(self, scale):
        self.scale = scale

    def get_scale(self):
        return self.scale

    def set_gain_db(self, db_reduction):
        amplitude_reduction = 10 ** (-float(db_reduction) / 20)
        self.gain = amplitude_reduction

    def set_gain(self, gain):
        self.gain = gain

    def get_gain(self):
        return self.gain

    def get_sr(self):
        return self.sr

    def get_id(self):
        return self.id

    def get_tune(self):
        return self.st_shift

    def get_path(self):
        return self.path

    def get_repr(self):
        return f'{self.get_tune()}'
    
    def get_heir(self):
        return self
    
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

