from classes import *
import audio

class Calliope(Algorithm):

    def __init__(self):
        self.datasets = {}
        self.sections = {}
    
    def create_loopkit(self, name='loopkit', loopkit_preset=None):
        loopkit = Loopkit(name)
        loopkit.fill(loopkit_preset)
        return loopkit

    def create_dataset(self, name):
        dataset = Dataset()
        for loopkit_preset in LOOPKITS:
            loopkit = self.create_loopkit(name='loopkit', loopkit_preset=loopkit_preset)
            dataset.add_loopkit(loopkit)
        self.datasets[name] = dataset
    
    def create_loopseq(self, loopkit, intensity_map):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.data.getName())
        loops = list(loopkit.data.getItems())
        loopseq.fill(intensity_map, loopkit=loops)
        return loopseq
        
    def create_section(self, dataset: Dataset, name):
        section = Section()
        for i, loopkit in enumerate(dataset):
            loopseq = self.create_loopseq(loopkit, INTENSITY[i])
            section.addItem(loopseq)
        section.set_bar_lenght(len(section.heir.heir.data))
        section.stretch_section()
        self.sections[name] = section

    def export_section(self, section: Section, name):
        track, trackouts = section.render_section()
        audio.export(name=(f'track{name}.wav'),audio=track)

    def getInfo():
        ...
    
    def start(self):
        for i in range(10):
            self.create_dataset(i)
            self.create_section(self.datasets[i], i)
            self.export_section(self.sections[i], i)

    def stop():
        ...
def main():
    calliope = Calliope()
    calliope.start()

if __name__ == '__main__':
    main()