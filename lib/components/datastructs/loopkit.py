from lib.components.abstract.abstract import Container
import lib.audio as audio
from lib.components.datastructs.loop import Loop
import lib.utils.util as util  

import logging
logger = logging.getLogger('my_logger')

class Loopkit(Container):
              
    def tune(self, tonality):
        for item in self.get_items():
            item_tone = util.extract_tonality_from_str(item.get_name())
            if item_tone is not None:
                tone_dif = int(util.scale_to_numeric(item_tone)) - int(util.scale_to_numeric(tonality))
                item.tune(tone_dif)

    def fill(self, path, n_loops, info):
        
        sr = info['sr']

        logger.info(f'Starting"{self.get_name()}" filling process...')
        logger.info(f'Loading {n_loops} loops from {path}')

        for i in range(int(n_loops)):
            loop = audio.file.load_loop_from_path(path=path, sr=sr)
            
            loop_tone = util.extract_tonality_from_str(loop.get_name())
            if loop_tone is not None and not isinstance(self, Drumkit):
                logger.info(f'tonality detected: {loop_tone}')
                if 'scale' not in info:
                    info['scale'] = util.extract_tonality_from_str(loop.get_name())
                    logger.info(f'WARN: global scale set to {info["scale"]} as {loop.get_name()}')
                
                tone_dif = int(util.scale_to_numeric(info['scale']) - util.scale_to_numeric(loop_tone))
                loop.tune(st_shift=tone_dif)
                logger.info(f'Tuned {loop.get_name()} to {info["scale"]} > {tone_dif}st')
                
                
            logger.info(f'Trimming {loop.get_name()} around 12s')
            min_len = int(info['sr'] * 12)
            loops = loop.trim(min_len)
            if loops is not None:
                for i, new_data in enumerate(loops):
                    new_loop = Loop(id=0, name=f'{loop.get_name()}_v{i+2}', data=new_data, sr=sr, path=loop.get_path())
                    self.add_item(new_loop)
            self.add_item(loop)

    def normalize_loop_length(self, info):
        
        if 'bar_lenght' not in info:
            info['bar_lenght'] = self.get_heir().get_len()
            logger.info(f'WARN: global bar lenght set to {info["bar_lenght"]} samples ({info["bar_lenght"]/info["sr"]} sec))')

        logger.info(f'Trimming loops lenght to {info["bar_lenght"]/info["sr"]} samples')
        for item in self.get_items():
            loops = item.trim(info['bar_lenght'])
            if loops is not None:
                for new_data in loops:
                    new_loop = Loop(id=0, name=item.get_name(), data=new_data, sr=info['sr'], path=item.get_path())
                    
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

