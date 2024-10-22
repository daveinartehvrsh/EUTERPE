from lib.components.abstract.container import Container
from lib.components.datastructs.dataset import Dataset
from lib.components.datastructs.trackout import Trackout
from lib.components.datastructs.loopkit import Loopkit
from lib.components.datastructs.loop import Track
import numpy as np
import logging
logger = logging.getLogger('my_logger')


class Mixer(Container):

    def __init__(self, name='section_as_a_track'):
        super().__init__(name)

    def sequence_loopkit(self, loopkit, loop_rep, info):
        loopseq = Trackout()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        loopseq.fill(loopkit=loops, loop_rep = loop_rep,
                        structure=info[loopkit.get_name()]['structure'],
                        tune_scheme=info[loopkit.get_name()]['tune_scheme'])
        return loopseq
    
    def fill(self, dataset: Dataset, loop_rep, info):
        self.ctrl_track = np.zeros([dataset.bar_length*loop_rep])
        for item in dataset.get_items():
            sequence = self.sequence_loopkit(item, loop_rep, info)
            self.add_item(sequence)

    def render_section(self):
        trackouts = Loopkit()
        beat = self.ctrl_track * 0

        for i, item in enumerate(self.get_items()):       
            trackout = item.render_sequence()
            trackouts.add_item(trackout)
            beat = np.add(beat, trackout)
            track = Track(id=i, name=i, data=beat, sr=0, path=None, scale=None, st_shift=0)
        return track, trackouts
    
