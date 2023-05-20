from lib.components.abstract.abstract import Container
from lib.components.datastructs.dataset import Dataset
from lib.components.datastructs.trackout import Trackout
from lib.components.datastructs.loopkit import Loopkit
from lib.components.datastructs.loop import Track
import lib.components.datastructs.schemes as schemes
import numpy as np
import logging
logger = logging.getLogger('my_logger')


class Mixer(Container):

    def __init__(self, system_info, name='section_as_a_track'):
        super().__init__(name)
        self.info = {
            'loop_rep': system_info['loop_beats'],
        }

        self.drum_track = {
            'gain': system_info['d_gain'],
            'structure': schemes.make_ranbinary(self.info['loop_rep'], system_info['d_intensity']),
            'intensity': system_info['d_intensity']
        }
        self.melody_track = {
            'gain': system_info['m_gain'],
            'structure': schemes.make_ones(self.info['loop_rep']),
            'intensity': system_info['m_intensity']
        }
        self.bass_track = {
            'gain': system_info['b_gain'],
            'structure': schemes.make_ranbinary(self.info['loop_rep'], system_info['b_intensity']),
            'intensity': system_info['b_intensity']
        }

    def set_bar_lenght(self, bar_lenght):
        self.info = {
            'bar_lenght': bar_lenght
        }

    def render_structure(self):
        structure = [self.drum_track['structure'], 
                     self.melody_track['structure'], 
                     self.bass_track['structure']]
        return structure
    
    def create_drum_loopseq(self, loopkit, loop_rep):
        loopseq = Trackout()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        tune_scheme = schemes.make_zeros(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.drum_track['gain'], 
                     structure=self.drum_track['structure'],
                     tune_scheme=tune_scheme)

        return loopseq
    
    def create_melody_loopseq(self, loopkit, loop_rep):
        loopseq = Trackout()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        tune_scheme = schemes.make_rantune(loop_rep, prob=float(self.melody_track['intensity']))
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.melody_track['gain'], 
                     structure=self.melody_track['structure'], 
                     tune_scheme=tune_scheme)
        return loopseq
    
    def create_bass_loopseq(self, loopkit, loop_rep):
        loopseq = Trackout()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        tune_scheme = schemes.make_zeros(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.bass_track['gain'], 
                     structure=self.bass_track['structure'],
                     tune_scheme=tune_scheme)
        return loopseq

    def fill(self, dataset: Dataset):
        rep = self.info['loop_rep']
        for item in dataset.get_items():
            if item.get_name() == 'drums':
                drum_seq = self.create_drum_loopseq(item, rep)
                self.add_item(drum_seq)
            elif item.get_name() == 'melody':
                melody_seq = self.create_melody_loopseq(item, rep)
                self.add_item(melody_seq)
            elif item.get_name() == 'bass':
                bass_seq = self.create_bass_loopseq(item, rep)
                self.add_item(bass_seq)
            else:
                logger.error('something strange happened')

    def render_section(self, bar_lenght):
        trackouts = Loopkit()
        beat = np.zeros([bar_lenght*self.info["loop_rep"]])

        for i, item in enumerate(self.get_items()):       
            trackout = item.render_sequence()
            trackouts.add_item(trackout)
            beat = np.add(beat, trackout)
            track = Track(id=i, name=i, data=beat, sr=0, path=None, scale=None, st_shift=0)
        return track, trackouts
    
