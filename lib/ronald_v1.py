from lib.classes import *
from lib.lss_v1 import Loopkit, Dataset
import lib.schemes as schemes
import random
import lib.audio as audio

class LoopSeq(Sequence):

    def fill(self, loopkit, loop_rep, gain, structure, tune_scheme=False):
        self.gain = gain
        self.structure = structure
        for i in track(range(loop_rep), 'filling sequence...'):
            loop = random.choice(loopkit)
            if tune_scheme[i]:
                tuned_data = audio.tune(loop, tune_scheme[i])
                tuned = Loop(id=loop.id, name=loop.name, data=tuned_data, sr=loop.sr, path=loop.path)           
                tuned.setTune(tune_scheme[i])
                self.add(tuned)
            else:
                self.add(loop)

    def render_sequence(self): 
        out = np.array([])
        for i, item in enumerate(self.getItems()):
            gain = self.structure[i] * self.gain
            out = np.append(out, item.data*float(gain))
        
        return out
    
    def getInfo(self):
        items = self.getItems()
        msg = ''
        for i, item in enumerate(items):
            loop_str = f'[TUNE: {item.getTune()}'
            while len(loop_str) < 22:
                loop_str += ' '
            loop_str += ']'
            msg += loop_str
            
        print(f'{self.getName()} | loop used: {item.getName()}\n{msg}\n')

class Section(Container):

    def set_bar_lenght(self, bar_lenght=None):
        if bar_lenght is None:
            first_loop = self.getHeir()
            bar_lenght = first_loop.getLen()
        self.bar_lenght = bar_lenght

    def render_section(self, bar_lenght, loop_rep):
        trackouts = Loopkit()
        beat = np.zeros([bar_lenght*loop_rep])

        for i, item in track(enumerate(self.getItems()), 'rendering section...'):       
            trackout = item.render_sequence()
            trackouts.addItem(trackout)
            beat = np.add(beat, trackout)
        return beat, trackouts


class Ronald_v1(BeatMaker):
    def __init__(self, system_info):
        self.info = {
            'loop_rep': int(system_info['loop_rep']),
        }

        self.drum_track = {
            'gain': system_info['d_gain'],
            'structure': schemes.make_ranbinary(self.info['loop_rep'], system_info['d_intensity'])
        }
        self.melody_track = {
            'gain': system_info['m_gain'],
            'structure': schemes.make_ones(self.info['loop_rep'])
        }
        self.bass_track = {
            'gain': system_info['b_gain'],
            'structure': schemes.make_ranbinary(self.info['loop_rep'], system_info['b_intensity'])
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
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        tune_scheme = schemes.make_zeros(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.drum_track['gain'], 
                     structure=self.drum_track['structure'],
                     tune_scheme=tune_scheme)

        return loopseq
    
    def create_melody_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        tune_scheme = schemes.make_rantune(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.melody_track['gain'], 
                     structure=self.melody_track['structure'], 
                     tune_scheme=tune_scheme)
        return loopseq
    
    def create_bass_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        tune_scheme = schemes.make_zeros(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, 
                     gain=self.bass_track['gain'], 
                     structure=self.bass_track['structure'],
                     tune_scheme=tune_scheme)
        return loopseq

    def create_section(self, dataset: Dataset, name):
        section = Section()
        rep = self.info['loop_rep']
        drum_seq = self.create_drum_loopseq(dataset.data[0].data, rep)
        melody_seq = self.create_melody_loopseq(dataset.data[1].data, rep)
        bass_seq = self.create_bass_loopseq(dataset.data[2].data, rep)

        section.addItem(drum_seq)
        section.addItem(melody_seq)
        section.addItem(bass_seq)

        return section

    def getInfo():
        ...