from lib.components.abstract.container import Container
import lib.audio as audio
from lib.components.datastructs.loop import Loop
import lib.utils.util as util  

import logging
logger = logging.getLogger('my_logger')

class Loopkit(Container):
              
    def tune(self, tonality):
        for item in self.get_items():
            item_tone = item.get_scale()
            if item_tone is not None:
                tone_dif = int(util.scale_to_numeric(item_tone)) - int(util.scale_to_numeric(tonality))
                item.tune(tone_dif)

    def fill(self, path, n_loops, info):
        
        sr = info['sr']
        

        logger.info(f'Starting "{self.get_name()}" loopkit filling process...')

        for i in range(int(n_loops)):
            loop = audio.file.rnd_loop(path=path, sr=sr)
            logger.info(f'Loaded {loop.get_name()}')
            logger.info(f'Audio lenght: {float("{:.2f}".format(len(loop.get_data())/loop.sr))} sec')
            logger.info(f'Tonality detected: {loop.get_scale()}')
            logger.info(f'bpm detected: {loop.get_bpm()}')
            if loop.get_scale() is not None and not isinstance(self, Drumkit):               
                if 'scale' not in info:
                    info['scale'] = loop.get_scale()
                    logger.info(f'GLOBAL scale set to {info["scale"]} as {loop.get_name()}')
                
                tone_dif = int(util.scale_to_numeric(info['scale']) - util.scale_to_numeric(loop.get_scale()))
                loop.tune(st_shift=tone_dif)
                logger.info(f'Loop tuned to {info["scale"]} > {tone_dif}st')

            min_len = int(info['sr'] * 12)
            loops = loop.trim(min_len)
            if loops is not None:
                for i, new_data in enumerate(loops):
                    new_loop = Loop(id=0, 
                                    name=f'{loop.get_name()}_v{i+2}', 
                                    data=new_data, sr=sr, 
                                    path=loop.get_path())
                    self.add_item(new_loop)
            self.add_item(loop)

        logger.info(f'"{self.get_name()}" loopkit filling process completed\n\n')

    def normalize_duration(self, bar_lenght):
        for item in self.get_items():
            loops = item.trim(bar_lenght)
            if loops is not None:
                for new_data in loops:
                    new_loop = Loop(id=0, name=item.get_name(), data=new_data, sr=item.sr, path=item.get_path())
                    
                    self.add_item(new_loop)

    def normalize_amplitude(self, gain):
        for item in self.get_items():
            item.normalize(gain)

class Drumkit(Loopkit):
    def stretch(self, lenght):
        for item in self.get_items():
            item.stretch(lenght, mode='resample')
        return item

class Melodykit(Loopkit):
    def stretch(self, lenght):
        for item in self.get_items():
            item.stretch(lenght, mode='key')
        return item

class Basskit(Loopkit):
    def stretch(self, lenght):
        for item in self.get_items():
            item.stretch(lenght, mode='key')
        return item

