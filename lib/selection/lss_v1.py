from lib.components.abstract import Container, AudioSelectionSystem
from lib.selection.loopkit import Loopkit, Drumkit, Melodykit, Basskit
import os
import logging
logger = logging.getLogger('my_logger')

class Dataset(Container):
    '''
    Dataset class is a container for loopkits.
    It is used to store all the loops that will be used to create the final song.
    '''
    def __init__(self, system_info=None, name='dataset'):
        super().__init__(name)
        self.info = {
            'BPM': system_info['BPM'],
            'loop_beats': system_info['loop_beats'],
            'sr': system_info['sr'],
            'path': system_info['dataset_path'],
        }
        self.drum_kit = {
            'path': system_info['d_path'],
            'n_loops': int(system_info['d_n_loops']),
        }
        self.melody_kit = {
            'path': system_info['m_path'],
            'n_loops': int(system_info['m_n_loops']),
        }
        self.bass_kit = {
            'path': system_info['b_path'],
            'n_loops': int(system_info['b_n_loops']),
        }

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
            logger.info(f'      Stretched {item.get_name()} loopkit to normalize lenghts to {self.get_heir().get_len()} samples')

    def fill(self):
        kits = [('bass', self.bass_kit['n_loops']), 
                ('drums',self.drum_kit['n_loops']), 
                ('melody', self.melody_kit['n_loops'])]
        
        for i, kit in enumerate(kits):
            loopkit = self.init_loopkit(kit[0])
            path = os.path.join(self.info['path'], kit[0])
            loopkit.fill(path=path, n_loops=kit[1], info=self.info)
            loopkit.normalize_loop_length(info=self.info)
            loopkit.normalize_amplitude()
            self.add_item(loopkit)
        
        self.normalize_length()
            
class LSS(AudioSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'name': 'LSS_v1',
            'gen_no': gen_no
        }
        self.dataset = Dataset(system_info, gen_no)
    
    def init_lss(self):
        self.dataset.fill()

    def get_info(self):
        return super().get_info() 
