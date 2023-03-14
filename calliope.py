from classes import *
from defaultPreset import *
import audio

class Calliope(Algorithm):

    def createDataset(self):
        dataset = Dataset()
        for x in range(TRACKS):
            for loopkit in LOOPKITS
            for path, tune in [LOOPKITS[loopkit]]:
                for 
                    loop = audio.loadLoop(path)
                dataset.addItem(loopkit, loop)

    def createStems(self):

