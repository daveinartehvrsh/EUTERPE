import lib.audio as audio
from lib.ronald_v1 import Ronald_v1, Section
from lib.lss_v1 import LSS_v1
import os
import time as time

from lib.log_info import DIVIDER
import logging
logger = logging.getLogger('my_logger')

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

        logger.info(f'rendering track no° {name}')    
        beat, trackouts = section.render_section(self.lss.dataset.info['bar_lenght'], 
                                                 self.beatmaker.track.info['loop_rep'])
        cwd = os.getcwd()
        new_dir = f'{self.system_info["preset"]}_{self.lss.info["gen_no"]}'

        os.chdir(self.system_info['outputfolder'])
        logger.info(f'Output folder: {os.getcwd()}')
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            os.chdir(new_dir)
        else:
            cur_time = time.time()
            logger.info(f'Output directory already exists! Creating new unique folder: {new_dir}_{cur_time}')
            os.mkdir(f'{new_dir}_{cur_time}')
            os.chdir(f'{new_dir}_{cur_time}')
                   
        audio.export(name=(f'{name}.wav'),audio=beat)
        logger.info(f'Track exported at: {os.getcwd()}/{name}.wav | lenght: {len(beat)/self.system_info["sr"]} sec')
        if len(trackouts.get_data()) > 0:
            os.mkdir('stems')
            os.chdir('stems')
            for i, trackout in enumerate(trackouts.get_items()):
                audio.export(name=(f'{name}_{i}.wav'),audio=trackout)
            
            logger.info(f'Trackouts exported at {os.getcwd()}\n')
        os.chdir(cwd)

    def get_info():
        ...
 
    def refresh(self, gen_no):
        self.lss = None
        self.lss = LSS_v1(self.system_info, gen_no)

        self.beatmaker = None
        self.beatmaker = Ronald_v1(self.system_info)


    def run(self, n_tracks): 
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler = logging.FileHandler('my_log_file.log')
        for i in range(n_tracks):
            logger.removeHandler(file_handler)
            file_handler = logging.FileHandler(f'my_log_file{i}.log')
            file_handler.setLevel(0)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.warning(f'{DIVIDER} GENERATING TRACK {i} {DIVIDER}\n')
            logger.info(f'Starting loop selection...')
            self.init_lss(gen_no=i)

            logger.info(f'Starting track creation...')
            self.beatmaker.make_track(self.lss.dataset)
            self.export_section(self.beatmaker.track, i)
            self.refresh(i)
        
def main():
    ...
    
if __name__ == '__main__':
    main()