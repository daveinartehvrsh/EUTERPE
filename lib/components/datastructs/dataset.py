from lib.components.abstract.abstract import Container
from lib.components.datastructs.loopkit import Loopkit, Drumkit, Melodykit, Basskit 
import os
import logging
logger = logging.getLogger('my_logger')

class Dataset(Container):
    '''
    Dataset class is a container for loopkits.
    It is used to store all the loops that will be used to create the final song.
    '''

    def init_loopkit(self, name='loopkit'):
        if name == 'drums':
            loopkit = Drumkit(name)
        elif name == 'melody':
            loopkit = Melodykit(name)
        elif name == 'bass':
            loopkit = Basskit(name)
        else:
            loopkit = Loopkit(name)
        return loopkit
    
    def normalize_length(self):
        for item in self.get_items():
            item.stretch(lenght = self.get_heir().get_len())
            logger.info(f'  Stretched {item.get_name()} loopkit to {self.get_heir().get_len()} samples')

    def fill(self, info):
        kits = info['kits'].keys()

        for name in kits:
            loopkit = self.init_loopkit(name)
            loopkit.fill(path=info['kits'][name]['path'], n_loops=info['kits'][name]['n_loops'], info=info)
            loopkit.normalize_loop_length(info=info)
            loopkit.normalize_amplitude(gain=info['kits'][name]['gain'])
            self.add_item(loopkit)
        
        self.normalize_length()
            
