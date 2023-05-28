from abc import ABC, abstractmethod
import lib.audio as audio
import logging
logger = logging.getLogger('my_logger')

class Component(ABC):

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
    
    def get_len(self):
        return len(self.data)
    
    def __len__(self):
        return self.get_len(self)
    
    def get_heir(self):
        return self

    @abstractmethod
    def get_info(self):
        ...

class AudioComponent(Component):
    def __init__(self, name, data, sr, gain=1, path=None):
        self.name = name
        self.data = data
        self.sr = sr
        self.gain = gain
        self.path = path

    def set_gain(self, gain):
        self.gain = gain

    def get_gain(self):
        return self.gain

    def get_sr(self):
        return self.sr

    def set_gain_db(self, db_reduction):
        amplitude_reduction = 10 ** (-float(db_reduction) / 20)
        self.gain = amplitude_reduction
    
    def normalize(self, gain=None):
        if gain is not None:
            self.set_gain_db(gain)
            self.set_data(audio.transform.normalize(self)*self.get_gain())
            logger.debug(f'Normalized {self.get_name()} peaks to -{gain} dB')
        else:    
            self.set_data(audio.transform.normalize(self))
            logger.debug(f'Normalized {self.get_name()} peaks to 0 dB')

    def get_info(self):
        ...

class ValueComponent(Component):
    ...

class Algorithm(Component):
    ...

class BeatMaker(Algorithm):
    def create_section(self, name):
        ...

class AudioSelectionSystem(Algorithm):
    def create_dataset(self, name):
        ...
