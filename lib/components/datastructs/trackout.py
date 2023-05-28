import random
import lib.audio as audio
from lib.components.datastructs.loop import Loop
from lib.components.abstract.abstract import Sequence
import numpy as np
import logging
logger = logging.getLogger('my_logger')

class Trackout(Sequence):

    def fill(self, loopkit, loop_rep, gain, structure, tune_scheme):
        
        logger.info(f'filling {self.get_name()} sequence')

        self.gain = gain
        self.structure = structure
        for i in range(loop_rep):
            loop = random.choice(loopkit)
            if self.structure.get_data()[i]:
                logger.info(f' |{i+1}|: {loop.get_name()} > {tune_scheme.get_data()[i]}st')
            elif not self.structure.get_data()[i]:
                logger.info(f' |{i+1}|: empty')
            else:
                logger.error('something strange happened')
            tuned_data = audio.tune.st_shift(loop, tune_scheme.get_data()[i])
            tuned = Loop(id=loop.id, name=loop.get_name(), data=tuned_data, sr=loop.sr, path=loop.path)           
            self.add(tuned)
        
        logger.info(f'Completed {self.get_name()} sequencencing\n')

    def render_sequence(self): 
        out = np.array([])
        for i, item in enumerate(self.get_items()):
            gain = self.structure.get_data()[i]# * self.gain
            out = np.append(out, item.get_data()*float(gain))
        
        return out
    
    def get_info(self):
        ...

