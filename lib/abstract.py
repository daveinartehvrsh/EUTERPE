from abc import ABC, abstractmethod

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

class ValueComponent(Component):
    ...

class Algorithm(Component):
    ...

class BeatMaker(Algorithm):
    def create_section(self, name):
        ...

class LoopSelectionSystem(Algorithm):
    def create_dataset(self, name):
        ...
   