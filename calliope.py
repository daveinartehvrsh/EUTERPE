from classes import *
import audio
import presets
from scheme import *

class Calliope(Algorithm):

    def __init__(self):
        self.datasets = {}
        self.sections = {}
        self.intensity_schemes = []
    
    def create_loopkit(self, name='loopkit', loopkit_preset=None):
        loopkit = Loopkit(name)
        loopkit.fill(loopkit_preset)
        return loopkit

    def create_dataset(self, name, dataset_preset=None):
        dataset = Dataset()
        for loopkit_preset in dataset_preset:
            loopkit = self.create_loopkit(name='loopkit', loopkit_preset= dataset_preset[loopkit_preset])
            dataset.add_loopkit(loopkit)
        self.datasets[name] = dataset
    
    def create_loopseq(self, loopkit, intensity_map, repetitions):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        loopseq.fill(intensity_map, loopkit=loops, repetitions = repetitions)
        return loopseq
        
    def create_section(self, dataset: Dataset, name, repetitions):
        section = Section()
        for i, loopkit in enumerate(dataset):
            loopseq = self.create_loopseq(loopkit.data, self.intensity_schemes[i], repetitions)
            section.addItem(loopseq)
        first_loop = section.getHeir()
        section.set_bar_lenght(first_loop.getLen())
        section.stretch_section()
        self.sections[name] = section

    def export_section(self, section: Section, name):
        track, trackouts = section.render_section(self.intensity_schemes)
        cwd = os.getcwd()
        os.chdir('out')
        audio.export(name=(f'track{name}.wav'),audio=track)
        os.chdir(cwd)

    def add_scheme(self, scheme_str: str):    
            scheme = Scheme()
            scheme.load_from_str(scheme_str)
            self.intensity_schemes.append(scheme)
            
    def getInfo():
        ...
    
    def start(self, system_info, dataset_preset=None, rep=None): 
        #default_loading
        if dataset_preset is None:
            dataset_preset = presets.get_default_dataset(system_info['default_dataset'])
        if rep is None:
            rep = system_info['n_tracks']
        for scheme_str in presets.get_schemes(system_info['default_track']):
            self.add_scheme(scheme_str)
        #algorythm start
        for i in range(rep):
            self.create_dataset(i, dataset_preset=dataset_preset)
            self.create_section(self.datasets[i], i, repetitions=system_info['repetitions'])
            self.export_section(self.sections[i], i)
        

    def stop():
        ...

def main():
    system_info = presets.get_default_config()    
    calliope = Calliope()
    calliope.start(system_info)

if __name__ == '__main__':
    main()