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
    def fill(self, path, tune_scheme):
        #cwd = os.getcwd()
        #path = os.path.join(cwd, path)
        loop_name = random.choice(os.listdir(path))
        path = path + "/" + loop_name
        data, sr = audio.loadLoop(path)          
        for tune in tune_scheme.data:
            loop = Loop(data, sr, path)
            loop.data = audio.tune(loop, tune)
            name = loop_name + f' [{tune}]'
            loop.setName(name)
            loop.setTune(tune)
            self.addItem(loop)

class Dataset(Container):
    def add_loopkit(self, loopkit):
        self.addItem(loopkit)
    
class LoopSeq(Sequence):

    def fill(self, loopkit, repetitions, gain):
        self.gain = gain
        self.seq_info = {}
        for i in track(range(repetitions), 'filling sequence...'):
            loop = random.choice(loopkit)
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


def main():
    ...
if __name__ == '__main__':
    main()