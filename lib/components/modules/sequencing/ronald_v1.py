from lib.components.abstract.abstract import BeatMaker
from lib.components.datastructs.mixer import Mixer
from lib.components.datastructs.dataset import Dataset
import lib.components.datastructs.schemes as schemes
import numpy as np
import logging
logger = logging.getLogger('my_logger')

class Ronald(BeatMaker):
    def __init__(self, system_info):
        self.loop_rep = int(system_info['bars']/system_info['loop_beats'])
        self.info = {
            'bars': system_info['bars'],
        }

        
    def make_track(self, dataset: Dataset):
        tracks = {}
        for item in dataset.get_items():
            tracks[item.get_name()] = {
                'structure': schemes.make_ranbinary(self.loop_rep, item.intensity),
                'tune_scheme': schemes.make_rantune(self.loop_rep, tunes = item.tunes, prob = 0.7)
            }
        self.track = Mixer()
        self.track.fill(dataset=dataset, loop_rep=self.loop_rep, info=tracks)

    def get_info():
        ...