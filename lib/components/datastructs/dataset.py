from lib.components.abstract.container import Container
from lib.components.datastructs.loopkit import Loopkit, Drumkit, Melodykit, Basskit 
import os
import logging
logger = logging.getLogger('my_logger')
import lib.utils.util as util

class Dataset(Container):
    '''
    Dataset class is a container for loopkits.
    It is used to store all the loops that will be used to create the final song.
    '''

    def init_loopkit(self, name='loopkit', kit_info=None):
        if name == 'drums':
            loopkit = Drumkit(name)
        elif name == 'melody':
            loopkit = Melodykit(name)
        elif name == 'bass':
            loopkit = Basskit(name)
        else:
            loopkit = Loopkit(name)

        loopkit.intensity = kit_info['intensity']
        loopkit.tunes = kit_info['tunes']
        return loopkit
    
    def stretch(self):
        for item in self.get_items():
            item.stretch(lenght = self.bar_length)
            logger.info(f'Stretched {item.get_name()} loopkit to global lenght')

    def fill(self, info):
        kits = info['channels'].keys()

        for name in kits:
            loopkit = self.init_loopkit(name, info['channels'][name])
            loopkit.fill(path=info['channels'][name]['path'], n_loops=info['channels'][name]['n_loops'], info=info)
            
            loopkit.normalize_amplitude(gain=info['channels'][name]['gain'])
            self.add_item(loopkit)
        
        if 'bar_length' in info.keys():
            self.bar_length = info['bar_length']
        else:
            self.bar_length = self.get_heir().get_len()
        
        for loopkit in self.get_items():
            loopkit.normalize_duration(self.bar_length)

        self.stretch()
        self.update_count()

        logger.info(f'Dataset filled with {len(self.get_loops())} loops\n\n')
    
    def get_loops(self):
        loops = []
        for loopkit in self.get_items():
            loops += loopkit.get_items()
        return loops

    def update_count(self):
        for loopkit in self.get_items():
            for loop in loopkit.get_items():
                util.count_to_csv(string=loop.get_name(), kit=loopkit.get_name(), csv_file=f'data/loop_count.csv')

    def to_csv(self, csv_name):
        for loopkit in self.get_items():
            kit_name = loopkit.get_name()
            for item in loopkit.get_items():
                loop_name = item.get_name()
                util.count_to_csv(loop_name, kit_name, csv_name)