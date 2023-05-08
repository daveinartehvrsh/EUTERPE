from lib.components.abstract import Container, AudioSelectionSystem
import lib.audio.audio as audio
from lib.audio.audio import Loop
import lib.utils.util as util

import logging
logger = logging.getLogger('my_logger')

class Loopkit(Container):
              
    def stretch_loop(self, loop, lenght):
        ...

    def stretch_all(self, bar_lenght):
        for item in self.get_items():
            self.stretch_loop(item, bar_lenght)  

    def tune(self, tonality):
        for item in self.get_items():
            item_tone = util.extract_tonality_from_str(item.get_name())
            if item_tone is not None:
                tone_dif = int(util.scale_to_numeric(item_tone)) - int(util.scale_to_numeric(tonality))
                item.tune(tone_dif)

    def fill(self, path, n_loops, info):
        
        sr = info['sr']

        logger.info(f'\n! Starting "{self.get_name()}kit" filling process...')
        logger.info(f'Loading {n_loops} loops from {path}')

        for i in range(int(n_loops)):
            loop = audio.load_loop_from_path(path=path, sr=sr)
            
            loop_tone = util.extract_tonality_from_str(loop.get_name())
            if loop_tone is not None and not isinstance(self, Drumkit):
                logger.info(f'tonality detected: {loop_tone}')
                if 'scale' not in info:
                    info['scale'] = util.extract_tonality_from_str(loop.get_name())
                    logger.info(f'Tonality set to {info["scale"]} as {loop.get_name()}')
                
                tone_dif = int(util.scale_to_numeric(info['scale']) - util.scale_to_numeric(loop_tone))
                loop.tune(st_shift=tone_dif)
                logger.info(f'Tuned {loop.get_name()} to {info["scale"]} > {tone_dif}st')
                
                min_len = int(info['sr'] * 12)
                loops = audio.trim_loop(loop, min_len)

                for new_data in loops:                    
                    new_loop = Loop(id=0, name=loop.get_name(), data=new_data, sr=sr, path=path)                        
                    self.add_item(new_loop)
            else:
                self.add_item(loop)

    def normalize_loop_length(self, info):
        if 'bar_lenght' not in info:
            info['bar_lenght'] = self.get_heir().get_len()

        for item in self.get_items()[1:]:
            loops = item.trim(info['bar_lenght'])
            if loops is not None:
                for new_data in loops:
                    new_loop = Loop(id=0, name=item.get_name(), data=new_data, sr=info['sr'], path=item.get_path())
                    self.add_item(new_loop)

    def normalize_amplitude(self):
        for item in self.get_items():
            item.normalize()

class Drumkit(Loopkit):
    def stretch_loop(self, loop, lenght):
        loop.stretch(lenght, mode='resample')
        return loop

class Melodykit(Loopkit):
    def stretch_loop(self, loop, lenght):
        loop.stretch(lenght, mode='key')
        return loop

class Basskit(Loopkit):
    def stretch_loop(self, loop, lenght):
        loop.stretch(lenght, mode='key')
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
        loopkit.fill(path = self.drum_kit['path'], n_loops = self.drum_kit['n_loops'], info=self.info) 
        loopkit.normalize_amplitude()
        loopkit.normalize_loop_length(self.info)
        loopkit.stretch_all(self.info['bar_lenght'])
        return loopkit
    
    def create_melody_loopkit(self, name='melody'):
        loopkit = Melodykit(name)       
        loopkit.fill(path = self.melody_kit['path'], n_loops = self.melody_kit['n_loops'], info=self.info)
        loopkit.normalize_amplitude()
        loopkit.normalize_loop_length(self.info)       
        loopkit.stretch_all(self.info['bar_lenght'])        
        return loopkit
    
    def create_bass_loopkit(self, name='bass'):
        loopkit = Basskit(name)
        loopkit.fill(path = self.bass_kit['path'], n_loops = self.bass_kit['n_loops'], info=self.info)
        loopkit.normalize_amplitude()
        loopkit.normalize_loop_length(self.info)
        loopkit.stretch_all(self.info['bar_lenght'])
        return loopkit

    def fill(self):
        bass_loopkit = self.create_bass_loopkit()
        drum_loopkit = self.create_drum_loopkit()
        melody_loopkit = self.create_melody_loopkit()
    
        self.add_item(drum_loopkit)
        self.add_item(melody_loopkit)
        self.add_item(bass_loopkit)

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
