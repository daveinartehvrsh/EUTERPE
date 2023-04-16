from lib.classes import *
import lib.schemes as schemes

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
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, gain=self.drum_track['gain'], structure=self.drum_track['structure'])
        
        #SETTING GLOBAL BAR LENGHT !!!!
        self.info['bar_lenght'] = len(loopseq.getHeir().data)

        return loopseq
    
    def create_melody_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        tune_scheme = schemes.make_rantune(loop_rep)
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, gain=self.melody_track['gain'], structure=self.melody_track['structure'], tune_scheme=tune_scheme)
        return loopseq
    
    def create_bass_loopseq(self, loopkit, loop_rep):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        loopseq.fill(loopkit=loops, loop_rep = loop_rep, gain=self.bass_track['gain'], structure=self.bass_track['structure'])
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

        #section.set_bar_lenght()
        section.stretch_section(self.info['bar_lenght'])
        return section

    def getInfo():
        ...