from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
from rich.traceback import install
import audio
import random
import os

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
        print(self.getName())

    def getRepr(self):
        return f'{len(self.getData())}'
    
    def setGain(self, gain):
        self.data *= gain

    def getLen(self):
        return len(self.data)

class SequenceNode():
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next_node = next
        self.prev_node = prev
    
    def __str__(self):
        return f'({self.data.getRepr()})'
    
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
    
    def getHeir(self):
        return self.root.data
    
    def getInfo(self):
        if self.root is None:
            return 'empty sequence'
        this_node = self.root
        print(this_node, end='->')
        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node, end='->')
        print()

    def getItems(self):
        this_node = self.root
        array=[]
        while this_node.next_node is not None:           
            array.append(this_node.data)   
            this_node = this_node.next_node
        array.append(this_node.data)  
        return array

class ContainerNode(Component):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent

    def __str__(self):  
        return f'({self.data})'
    
    def getInfo(self):
        if isinstance(self.data, Component):
            return self.data.getInfo()
        else:
            print('(audio)')
            
class ContainerIter():
    def __init__(self, container):
        self.data = container.data
        self.size = container.size
        self.index = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index <= self.size:
            item = self.data[self.index - 1]
            self.index += 1
            return item
        raise StopIteration

class Container(Component):
    def __init__(self, name='container'):
        self.name = name
        self.size = 0
        self.data = []

    def getSize(self):
        return self.size

    def addItem(self, item):
        self.data.append(ContainerNode(item, self.getName()))
        if self.size == 0:
            self.heir = item
        self.size += 1

    def getHeir(self):
        return self.heir.getHeir()

    def get_nodes(self):
        return self.data
    
    def getItems(self):
        array=[]
        for item in self.get_nodes():
            array.append(item.data)
        return array
    
    def getInfo(self):
        print(self.getName())
        for x in self.data: 
            x.getInfo()

    def __iter__(self):
        return ContainerIter(self)

class Loopkit(Container):
    
    def fill(self, loopkit_preset):
        path = loopkit_preset['path']
        loop_name = random.choice(os.listdir(path))
        path = path + "/" + loop_name
        data, sr = audio.loadLoop(path)
        #audio.export(name=loop_name, audio=data)           
        for tune in loopkit_preset['tune_scheme']:
            loop = Loop(data, sr, path)
            loop.data = audio.tune(loop, tune)
            name = loop_name + str(tune)
            loop.setName(name)
            self.addItem(loop)
        #self.getInfo()

class Dataset(Container):
    def add_loopkit(self, loopkit):
        self.addItem(loopkit)

    def fill(self, preset):
        ...
    
class LoopSeq(Sequence):
        
    def fill(self, intensity_map, loopkit, repetitions=2):
        repetitions = len(intensity_map.getData())
        for i in range(repetitions):
            loop = random.choice(loopkit)
            self.add(loop)
    
    def stretch_sequence(self, to_len):
        for item in self.getItems():
            stretched = audio.stretch(item, to_len)
            item.setData(stretched)

    def render_sequence(self, intensity_map): 
        out = np.array([])
        for i, item in enumerate(self.getItems()):
            gain = intensity_map.data[i]
            out = np.append(out, item.data*float(gain))
        return out

class Section(Container):

    def set_bar_lenght(self, bar_lenght=None):
        self.bar_lenght = bar_lenght

    def stretch_section(self):
        for item in self.getItems():
            item.stretch_sequence(self.bar_lenght)

    def render_section(self, intensity_schemes):
        trackouts = Loopkit()
        track = np.zeros([self.bar_lenght*self.heir.size])
        for i, item in enumerate(self.getItems()):       
            trackout = item.render_sequence(intensity_schemes[i])
            trackouts.addItem(trackout)
            track = np.add(track, trackout)
        return track, trackouts

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
    ...
    def setAlgorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm

    def start():
        ...
    def stop():
        ...

def main():
    ...
if __name__ == '__main__':
    main()