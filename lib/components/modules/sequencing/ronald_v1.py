from lib.components.abstract.abstract import BeatMaker
from lib.components.datastructs.mixer import Mixer
from lib.components.datastructs.dataset import Dataset
import lib.components.datastructs.schemes as schemes
import numpy as np
import logging
logger = logging.getLogger('my_logger')

class Ronald(BeatMaker):
    def __init__(self, system_info):
        loop_rep = int(system_info['bars']/system_info['loop_beats'])
        self.info = {
            'loop_rep': loop_rep,
            'bars': system_info['bars'],
            'tracks': {
                'bass': {
                    'gain': system_info['b_gain'],
                    'structure': schemes.make_ranbinary(loop_rep, float(system_info['b_intensity'])),
                    'tune_scheme': schemes.make_zeros(loop_rep),
                    'intensity': system_info['b_intensity']
                },
                'drums': {
                    'gain': system_info['d_gain'],
                    'structure': schemes.make_ranbinary(loop_rep, float(system_info['d_intensity'])),
                    'tune_scheme': schemes.make_zeros(loop_rep),
                    'intensity': system_info['d_intensity']
                },
                'melody': {
                    'gain': system_info['m_gain'],
                    'structure': schemes.make_ones(loop_rep),
                    'tune_scheme': schemes.make_rantune(loop_rep, float(system_info['m_intensity'])),
                    'intensity': system_info['m_intensity']
                }
            }
        }

        self.track = Mixer(self.info)

    def make_track(self, dataset: Dataset):
        self.track.fill(dataset, self.info)

    def get_info():
        ...