from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
from rich.traceback import install
import audio
import random
import os

SAMPLERATE = 44100
TRACKS = 10
DATASETPATH = 'D:\RONALD_(versionprealpha)\RONALD_prealpha\data\loops'

DRUMS = {
    'D:/RONALD_(versionprealpha)/RONALD_prealpha/data/loops/drums': [0]
}


D_INTENSITY = [0, 0, 1, 1, 1, 0, 0]
M_INTENSITY = [1, 1, 1, 1, 1, 1, 1]

MELODY = {
    'D:/RONALD_(versionprealpha)/RONALD_prealpha/data/loops/melodie': [0]
}

LOOPKITS = [DRUMS, MELODY]

install()

class Component(ABC):

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data
    
    @abstractmethod
    def getInfo(self):
        ...

class AudioComponent(Component):
    ...

class Loop(AudioComponent):
    def __init__(self, data, sr, path):
        self.data = data
        self.sr = sr
        self.path = path
    
    def getInfo(self):
        return self.getName()

class SequenceNode():
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next_node = next
        self.prev_node = prev
    
    def __str__(self):
        return f'({self.data})'
    def getInfo(self):
        return self.data.getInfo()
    
class Sequence(Component):
    
    def __init__(self, r=None):
        self.root = r
        self.last = r
        self.size = 0

    def add(self, item):
        if self.size == 0:
            self.root = SequenceNode(item)
            self.last = self.root
        else:
            new_node = SequenceNode(item, prev= self.last)
            self.last.next_node = new_node
            self.last = new_node
        self.size += 1
    
    def find(self, item):
        this_node = self.root
        while this_node is not None:
            if this_node.data == item:
                return item
            elif this_node.next_node == None:
                return False
            else:
                this_node = this_node.next_node

    def remove(self, item):
        this_node = self.root
        while this_node is not None:
            if this_node.data == item:
                if this_node.prev_node is not None:
                    if this_node.next_node is not None:
                        this_node.prev_node.next_node = this_node.next_node
                        this_node.next_node.prev_node = this_node.prev_node
                    else:
                        this_node.prev_node.next_node = None
                        self.last = this_node.prev_node
                else:
                    self.root = this_node.next_node
                    this_node.next_node.prev_node = self.root
                self.size -= 1
                return True
            else:
                this_node = this_node.next_node
        return False
    
    def getInfo(self):
        if self.root is None:
            return 'empty sequence'
        this_node = self.root
        print(this_node.getInfo(), end='->')
        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node.getInfo(), end='->')
        print()

class ContainerNode(Component):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent

    def __str__(self):  
        return f'({self.data})'
    
    def getInfo(self):
        return self.data.getInfo()

class Container(Component):
    def __init__(self, name='container'):
        self.name = name
        self.size = 0
        self.data = []

    def getSize(self):
        return self.size

    def addItem(self, item):
        self.data.append(ContainerNode(item, self.getName()))
        self.size += 1

    def getItems(self):
        return self.getData()
    
    def getInfo(self):
        print(self.getName())
        for x in self.data: 
            x.data.getInfo()
            
class Loopkit(Container):
    
    def fill(self, loopkit_preset, selection_method='random'):
        for path, tune_scheme in loopkit_preset.items():
            if selection_method == 'random':
                loop_name = random.choice(os.listdir(path))
                path = path + "/" + loop_name
            loop = audio.loadLoop(path)
            loop.setName(loop_name)

            for tune in tune_scheme:
                loop.data = audio.tune(loop, tune)
                self.addItem(loop)

class Dataset(Container):
    
    def create_loopkit(self, name='loopkit', loopkit_preset=None):
        loopkit = Loopkit(name)
        loopkit.fill(loopkit_preset)
        self.addItem(loopkit)
    
class LoopSeq(Sequence):
        
    def fill(self, intensity_map, loopkit):
        for intensity in intensity_map:
            loop = random.choice(loopkit)
            self.add(loop)

class Section(Container):
    ...
    
class ValueComponent(Component):
    ...

class Score(ValueComponent):
    ...

class ScoreVector(Container):
    ...

class ScoreMap(Container):
    ...

class TextComponent(Component):
    @abstractmethod
    def __repr__(self) -> str:
        ...

class Preset(Container):
    ...

@dataclass
class InfoElement(TextComponent):
    name: str

class Info:
    ...

class Algorithm(Component):
    version: str = field(default_factory=lambda: '0.0.0')

class Generation:

    def setAlgorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm

    def start():
        ...
    def stop():
        ...

def main():
    dataset = Dataset()
    for loopkit_preset in LOOPKITS:
        dataset.create_loopkit(name='loopkit', loopkit_preset=loopkit_preset) 
    
    section = Section()
    for loopkit in dataset.getItems():
        loopseq = LoopSeq()
        loopseq.setName(loopkit.data.getName())
        loopseq.fill(M_INTENSITY, loopkit=loopkit.data.getItems())
        section.addItem(loopseq)
    
    section.getInfo()

if __name__ == '__main__':
    main()