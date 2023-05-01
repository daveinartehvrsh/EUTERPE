from lib.abstract import AudioComponent, Container, LoopSelectionSystem
import lib.audio as audio
from lib.audio import Loop
import lib.util as util
from lib.util import DIVIDER
import random
import os

class Loopkit(Container):
              
    def stretch_loop(self, loop, lenght):
        loop.tone_stretch(lenght)

    def stretch_loop_at_index(self, index, lenght):
        loop = self.getItems()[index]
        self.stretch_loop(loop, lenght) 

    def stretch_all(self, bar_lenght):
        for item in self.getItems():
            self.stretch_loop(item, bar_lenght)  

    def tune(self, tonality):
        for item in self.getItems():
            item_tone = util.extract_tonality_from_str(item.getName())
            if item_tone is not None:
                tone_dif = int(util.scale_to_numeric(item_tone)) - int(util.scale_to_numeric(tonality))
                item.tune(tone_dif)
                item.setTune(tone_dif)

    def stretch_all(self, bar_lenght):
        for item in self.getItems():
            item.stretch(bar_lenght)

    def trim_loops(self, bar_lenght):
        for item in self.getItems():
            loops = audio.trim_loop(data=item, ref_len=bar_lenght, log=True)
            if loops is not None:
                for loop in loops:
                    new_loop = Loop(id=0, name=item.getName(), data=loop, sr=item.sr, path=item.path)
                    self.addItem(new_loop)
                self.remove(item)

    def fill(self, path, n_loops, info, log=False):

        if log:
            print(f'\n! Starting {self.getName()}kit filling process...')
            print(f'| Loading {n_loops} loops from {path}')

        if info['BPM'] != 'auto':  
            min_len = int(info['sr'] * (60 / info['BPM']) * info['loop_beats']*4)
            info['bar_lenght'] = min_len

            if log:
                print(f'! global bar lenght set to {info["bar_lenght"]/info["sr"]} sec')

        for i in range(int(n_loops)):
            loop = audio.load_loop_from_path(path=path, sr=info['sr'])
            if log:
                print(f'\n! loaded data: {loop.getName()}')
            if 'bar_lenght' not in info:
                min_len = int(info['sr'] * 10)
                loops = audio.check_min_len(loop, min_len, log=True)
                
                info['bar_lenght'] = len(loops[0])
                if log:
                    print(f'! global bar lenght set to {len(loops[0])/loop.sr} sec')

            else:                   
                loops = audio.check_min_len(loop, info['bar_lenght'], log=True)

            if log:
                    print(f'! adding {len(loops)} loops to loopkit')
            for new_data in loops:                    
                new_loop = Loop(id=0, name=loop.getName(), data=new_data, sr=loop.sr, path=path)                        
                self.addItem(new_loop)

        if log:
            print(f'\n! filling completed successfully\n')

class Drumkit(Loopkit):
    def stretch_loop(self, loop, lenght):
        loop.stretch(lenght)
        return loop

class Melodykit(Loopkit):
    def stretch_loop(self, loop, lenght):
        loop.tone_stretch(lenght)
        return loop

class Basskit(Loopkit):

    def stretch_loop(self, loop, lenght):
        loop.tone_stretch(lenght)
        return loop

class Dataset(Container):

    def __init__(self, system_info=None, name='dataset'):
        super().__init__(name)
        self.info = {
            'BPM': system_info['BPM'],
            'loop_beats': system_info['loop_beats'],
            'sr': system_info['sr'],
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
        loopkit = Drumkit(name)
        loopkit.fill(path = self.drum_kit['path'], n_loops = self.drum_kit['n_loops'], info=self.info, log=True)
        #loopkit.trim_loops(self.info['bar_lenght'])  
        loopkit.stretch_all(self.info['bar_lenght'])
        return loopkit
    
    def create_melody_loopkit(self, name='melody'):
        loopkit = Melodykit(name)       
        loopkit.fill(path = self.melody_kit['path'], n_loops = self.melody_kit['n_loops'], info=self.info, log=True)
        #loopkit.trim_loops(self.info['bar_lenght'])        
        if 'scale' not in self.info:
            self.info['scale'] = util.extract_tonality_from_str(loopkit.getHeir().getName()) 
        loopkit.tune(self.info['scale'])
        loopkit.stretch_all(self.info['bar_lenght'])        
        return loopkit
    
    def create_bass_loopkit(self, name='bass'):
        loopkit = Basskit(name)
        loopkit.fill(path = self.bass_kit['path'], n_loops = self.bass_kit['n_loops'], info=self.info, log=True)
        #loopkit.trim_loops(self.info['bar_lenght'])
        if 'scale' not in self.info:
            self.info['scale'] = util.extract_tonality_from_str(loopkit.getHeir().getName())            
        loopkit.tune(self.info['scale'])
        loopkit.stretch_all(self.info['bar_lenght'])
        return loopkit

    def normalize_loops(self, log=False):
        return
        if log:
            print(f'{DIVIDER} NORMALIZING LOOPS INSIDE {self.getName()} {DIVIDER}')
        for item in self.getItems():        
            continue

    def fill(self):        
        drum_loopkit = self.create_drum_loopkit()
        melody_loopkit = self.create_melody_loopkit()
        bass_loopkit = self.create_bass_loopkit()
            
        self.addItem(drum_loopkit)
        self.addItem(melody_loopkit)
        self.addItem(bass_loopkit)

class LSS_v1(LoopSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'name': 'LSS_v1',
            'gen_no': gen_no
        }
        self.dataset = Dataset(system_info, gen_no)
    
    def init_lss(self):
        self.dataset.fill()

    def getInfo(self):
        return super().getInfo() 
