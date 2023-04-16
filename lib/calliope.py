from lib.classes import *
import lib.audio as audio
import lib.presets as presets
from lib.ronald_v1 import Ronald_v1
from lib.lss_v1 import LSS_v1

class Calliope(Algorithm):

    def __init__(self, system_info):
        self.system_info = system_info
        self.beatmaker = Ronald_v1(system_info)
        self.lss = LSS_v1(system_info)
        self.datasets = {}
        self.sections = {}
        self.tracks = ScoreMap()
        self.intensity_schemes = []
        
    def create_dataset(self, name):       
        self.datasets[name] = self.lss.create_dataset(name)
    
    def create_section(self, dataset: Dataset, name):
        self.sections[name] = self.beatmaker.create_section(dataset, name)

    def export_section(self, section: Section, name):
        #intensity_schemes = self.beatmaker.render_structure()       
        beat, trackouts = section.render_section()
        cwd = os.getcwd()
        out = os.path.join(self.system_info['outputfolder'], self.system_info['preset'])
        os.chdir(out)
        audio.export(name=(f'{name}.wav'),audio=beat)
        os.chdir(cwd)

    def getInfo():
        ...

    def stop(self):    
        ...
    
    def start(self): 
        for i in range(self.system_info['steps']):
            self.create_dataset(i)
            self.create_section(self.datasets[i], i)
            self.export_section(self.sections[i], i)
        
def main():
    ...
    
if __name__ == '__main__':
    main()