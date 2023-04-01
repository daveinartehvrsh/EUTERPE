from lib.classes import *

class LSS_v1(LoopSelectionSystem):

    def __init__(self, system_info):

        self.drum_kit = {
            'path': system_info['d_path'],
            'n_loops': system_info['d_n_loops'],
        }
        self.melody_kit = {
            'path': system_info['m_path'],
            'n_loops': system_info['m_n_loops'],
        }
        self.bass_kit = {
            'path': system_info['b_path'],
            'n_loops': system_info['b_n_loops'],
        }

    def create_drum_loopkit(self, name='drums'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.drum_kit['path'], n_loops = self.drum_kit['n_loops'])
        return loopkit
    
    def create_melody_loopkit(self, name='melody'):
        loopkit = Loopkit(name)       
        loopkit.fill(path = self.melody_kit['path'], n_loops = self.melody_kit['n_loops'])
        return loopkit
    
    def create_bass_loopkit(self, name='bass'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.bass_kit['path'], n_loops = self.bass_kit['n_loops'])
        return loopkit

    def create_dataset(self, name):
        dataset = Dataset()

        drum_loopkit = self.create_drum_loopkit()
        melody_loopkit = self.create_melody_loopkit()
        bass_loopkit = self.create_bass_loopkit()
    
        dataset.addItem(drum_loopkit)
        dataset.addItem(melody_loopkit)
        dataset.addItem(bass_loopkit)
        
        return dataset

    def getInfo(self):
        return super().getInfo() 
