from abc import ABC, abstractmethod
import numpy as np
import audio
import random
import os
from rich.progress import track

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

class SequenceNode():
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next_node = next
        self.prev_node = prev
    
    def __str__(self):
        return f'[{self.data.getRepr()}]'
    
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
        print(f'{self.getName()} - |', end='')
        this_node = self.root
        print(this_node, end='')
        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node, end='')
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
    def fill(self, path, tune_scheme):
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

class ValueComponent(Component):
    ...

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

class Algorithm(Component):
    ...

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