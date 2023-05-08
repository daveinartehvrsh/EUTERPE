from lib.components.abstract import Container, Sequence, BeatMaker
from lib.selection.lss_v1 import Loopkit, Dataset, Loop
import lib.utils.schemes as schemes
import random
import lib.audio.audio as audio
import numpy as np

import logging
logger = logging.getLogger('my_logger')

class LoopSeq(Sequence):

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
            gain = self.structure[i] * self.gain
            out = np.append(out, item.data*float(gain))
        
        return out
    
    def get_info(self):
        ...

class Section(Container):

    def __init__(self, system_info, name='section_as_a_track'):
        super().__init__(name)
        self.info = {
            'loop_rep': int(int(system_info['bars']) / system_info['loop_beats']),
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
        loopseq = LoopSeq()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        tune_scheme = schemes.make_zeros(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.drum_track['gain'], 
                     structure=self.drum_track['structure'],
                     tune_scheme=tune_scheme)

        return loopseq
    
    def create_melody_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
        loopseq.set_name(loopkit.get_name())
        loops = loopkit.get_items()
        tune_scheme = schemes.make_rantune(loop_rep, prob=float(self.melody_track['intensity']))
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.melody_track['gain'], 
                     structure=self.melody_track['structure'], 
                     tune_scheme=tune_scheme)
        return loopseq
    
    def create_bass_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
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
        drum_seq = self.create_drum_loopseq(dataset.data[0].data, rep)
        melody_seq = self.create_melody_loopseq(dataset.data[1].data, rep)
        bass_seq = self.create_bass_loopseq(dataset.data[2].data, rep)

        self.add_item(drum_seq)
        self.add_item(melody_seq)
        self.add_item(bass_seq)

    def render_section(self, bar_lenght, loop_rep):
        trackouts = Loopkit()
        beat = np.zeros([bar_lenght*loop_rep])

        for i, item in enumerate(self.get_items()):       
            trackout = item.render_sequence()
            trackouts.add_item(trackout)
            beat = np.add(beat, trackout)
        return beat, trackouts
    
class Ronald_v1(BeatMaker):
    def __init__(self, system_info):
        self.track = Section(system_info)

    def make_track(self, dataset: Dataset):
        self.track.fill(dataset)

    def get_info():
        ...