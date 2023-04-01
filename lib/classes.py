from lib.abstract import *
from lib.datastructs import *
import numpy as np
import lib.audio as audio
import random
import os
from rich.progress import track

class Loop(AudioComponent):
    def __init__(self, data, sr, path):
        self.data = data
        self.sr = sr
        self.path = path
    
    def setTune(self, tune):
        self.tune = tune

    def getTune(self):
        return self.tune

    def getLen(self):
        return len(self.data)
    
    def getInfo(self):
        print(self.getName())

    def getRepr(self):
        return f'{self.getTune()}'

class Loopkit(Container): 
    def fill(self, path, n_loops):
        # load as many loops as n_loops (config_file)         
        for i in range(n_loops):
            # get random loop from path (selection algorithms may be added later)
            loop_name = random.choice(os.listdir(path))
            loop_path = path + "/" + loop_name
            data, sr = audio.loadLoop(loop_path)
            loop = Loop(data, sr, path)
            loop.setName(loop_name)
            self.addItem(loop)

class Dataset(Container):
    def add_loopkit(self, loopkit):
        self.addItem(loopkit)
    
class LoopSeq(Sequence):

    def fill(self, loopkit, loop_rep, gain, tune_scheme=False):
        self.gain = gain
        self.seq_info = {}
        for i in track(range(loop_rep), 'filling sequence...'):
            loop = random.choice(loopkit)
            if tune_scheme:
                tuned_data = audio.tune(loop, tune_scheme[i])
                tuned = Loop(tuned_data, loop.sr, loop.path)
                tuned.setName(loop.getName())                
                tuned.setTune(tune_scheme[i])
                self.add(tuned)
            else: 
                self.add(loop)

    def stretch_sequence(self, to_len):
        for item in self.getItems():
            stretched = audio.stretch(item, to_len)
            item.setData(stretched)

    def render_sequence(self, intensity_scheme): 
        out = np.array([])
        for i, item in enumerate(self.getItems()):
            gain = intensity_scheme[i] * self.gain
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

    def stretch_section(self):
        for item in track(self.getItems(), 'stretching section...'):
            item.stretch_sequence(self.bar_lenght)

    def render_section(self, intensity_schemes):
        trackouts = Loopkit()
        beat = np.zeros([self.bar_lenght*self.heir.size])

        for i, item in track(enumerate(self.getItems()), 'rendering section...'):       
            trackout = item.render_sequence(intensity_schemes[i])
            trackouts.addItem(trackout)
            beat = np.add(beat, trackout)
        return beat, trackouts

class Score(ValueComponent):
    def __init__(self, name='score', value=0):
        self.name = name
        self.value = value
    
    def getInfo(self):
        print(f'{self.getName()} - {self.value}')

class ScoreVector(Container):
    def __init__(self, name='score vector', data=[]):
        self.name = name
        self.size = 0
        self.data = np.array(data)

class ScoreMap(Container):
    def __init__(self, name='score map'):
        self.name = name
        self.size = 0
        self.data = []

class BeatMaker(Algorithm):
    def create_section(self, name):
        ...

class LoopSelectionSystem(Algorithm):
    def create_dataset(self, name):
        ...

def main():
    ...

if __name__ == '__main__':
    main()