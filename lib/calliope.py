import lib.audio as audio
from lib.ronald_v1 import Ronald_v1, Section
from lib.lss_v1 import LSS_v1
import os

DIVIDER = '-----------------------------'

class Calliope():

    def __init__(self, system_info):
        self.system_info = system_info
        self.beatmaker = Ronald_v1(system_info)
        self.sections = {}
        self.intensity_schemes = []
        
    def init_lss(self, gen_no):       
        self.lss = LSS_v1(self.system_info, gen_no)
        self.lss.init_lss()
    
    def export_section(self, section: Section, name):    
        beat, trackouts = section.render_section(self.lss.dataset.info['bar_lenght'], 
                                                 self.beatmaker.track.info['loop_rep'])
        cwd = os.getcwd()
        out = os.path.join(self.system_info['outputfolder'], self.system_info['preset'])
        os.chdir(out)
        audio.export(name=(f'{name}.wav'),audio=beat)
        os.chdir(cwd)

    def getInfo():
        ...
 
    def refresh(self, gen_no):
        self.lss = None
        self.lss = LSS_v1(self.system_info, gen_no)

        self.beatmaker = None
        self.beatmaker = Ronald_v1(self.system_info)


    def run(self, n_tracks, log=False): 
        for i in range(n_tracks):

            if log:
                print(f'{DIVIDER} GENERATING TRACK {i} {DIVIDER}\n')
                print(f'! Starting loop selection...')
            self.init_lss(gen_no=i)

            if log:
                print(f'! Starting track cration...')
            self.beatmaker.make_track(self.lss.dataset)
            self.export_section(self.beatmaker.track, i)
            self.refresh(i)
        
def main():
    ...
    
if __name__ == '__main__':
    main()