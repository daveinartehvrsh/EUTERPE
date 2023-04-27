from lib.abstract import *
import lib.audio as audio
import numpy as np
from rich.progress import track

class Loop(AudioComponent):
    def __init__(self, id: int, name: str, data, sr: int, path: str):
        self.id = id
        self.name = name
        self.data = data
        self.sr = sr
        self.path = path
    
    def stretch(self, bar_lenght):
        self.setData(audio.stretch(self, bar_lenght))

    def getId(self):
        return self.id
    
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
    
    def getHeir(self):
        return self

class BeatMaker(Algorithm):
    def create_section(self, name):
        ...

class LoopSelectionSystem(Algorithm):
    def create_dataset(self, name):
        ...

def main():
    ...
    
if __name__ == "__main__":
    main()