from lib.classes import Container, Loop, LoopSelectionSystem
from lib.abstract import *
import lib.audio as audio
import random
import os

class Loopkit(Container):
                
    def fill(self, path, n_loops, info):       
        for i in range(int(n_loops)):
            loop_name = random.choice(os.listdir(path))
            loop_path = os.path.join(path, loop_name)
            data, sr = audio.loadLoop(loop_path)
            '''if info['bar_lenght']:
                loops, num = audio.trim_loop(info['bar_lenght'], data)
                for i in range(num):
                    loop = Loop(id=0, name=loop_name, data=loops[i], sr=sr, path=path)
                    loop = audio.stretch(loop, info['bar_lenght'])
                    self.addItem(loop)'''
            loop = Loop(id=0, name=loop_name, data=data, sr=sr, path=path)
            self.addItem(loop)

    def stretch(self, bar_lenght):
        for item in self.getItems():
            item.stretch(bar_lenght)

class Dataset(Container):
    pass

class LSS_v1(LoopSelectionSystem):

    def __init__(self, system_info):
        self.info = {
            'name': 'LSS_v1'
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

    def create_drum_loopkit(self, name='drums'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.drum_kit['path'], n_loops = self.drum_kit['n_loops'], info=self.info)
        self.info['bar_lenght'] = loopkit.getHeir().getLen()
        loopkit.stretch(self.info['bar_lenght'])
        return loopkit
    
    def create_melody_loopkit(self, name='melody'):
        loopkit = Loopkit(name)       
        loopkit.fill(path = self.melody_kit['path'], n_loops = self.melody_kit['n_loops'], info=self.info)
        loopkit.stretch(self.info['bar_lenght'])
        return loopkit
    
    def create_bass_loopkit(self, name='bass'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.bass_kit['path'], n_loops = self.bass_kit['n_loops'], info=self.info)
        loopkit.stretch(self.info['bar_lenght'])
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
