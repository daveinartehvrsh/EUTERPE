import random
import lib.audio.audio as audio
from lib.components.datastructs.loop import Loop
from lib.components.abstract.abstract import Sequence
import numpy as np
import logging
logger = logging.getLogger('my_logger')

class Trackout(Sequence):

    def fill(self, loopkit, loop_rep, gain, structure, tune_scheme=False):
        
        logger.info(f'filling {self.get_name()} sequence')

        self.gain = gain
        self.structure = structure
        for i in range(loop_rep):
            loop = random.choice(loopkit)
            if self.structure[i]:
                logger.info(f' |{i+1}|: {loop.get_name()} > {tune_scheme[i]}st')
            elif not self.structure[i]:
                logger.info(f' |{i+1}|: empty')
            else:
                logger.error('something strange happened')
            if tune_scheme[i]:
                tuned_data = audio.tune(loop, tune_scheme[i])
                tuned = Loop(id=loop.id, name=loop.name, data=tuned_data, sr=loop.sr, path=loop.path)           
                self.add(tuned)
            else:
                self.add(loop)
        
        logger.info(f'Completed {self.get_name()} sequencencing\n')

    def render_sequence(self): 
        out = np.array([])
        for i, item in enumerate(self.get_items()):
            gain = self.structure[i]# * self.gain
            out = np.append(out, item.data*float(gain))
        
        return out
    
    def get_info(self):
        ...

