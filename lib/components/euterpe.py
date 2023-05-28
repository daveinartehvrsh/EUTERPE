import lib.audio as audio
from lib.components.modules.selection.lss_v1 import LSS
from lib.components.datastructs.mixer import Mixer
from lib.components.modules.sequencing.ronald_v1 import Ronald

import os
import time as time

from lib.utils.log_info import DIVIDER
import logging
logger = logging.getLogger('my_logger')

class Euterpe():

    def __init__(self, system_info):
        self.system_info = system_info
        self.beatmaker = Ronald(system_info)
        self.sections = {}
        self.intensity_schemes = []
        
    def init_lss(self, gen_no):
        if self.system_info['bpm'] != 'auto':
            self.system_info['bar_lenght'] = self.system_info['bpm'] * self.system_info['sr'] * 16
            logger.info(f'GLOBAL: {self.system_info["bpm"]} bpm: Bar lenght set to {self.system_info["bar_lenght"]}')    
        self.lss = LSS(self.system_info, gen_no)
        self.lss.init_lss()
    
    def export_section(self, section: Mixer, name):
        beat, trackouts = section.render_section()
        beat = audio.transform.normalize(beat)
        os.chdir(self.system_info['outputdirectory'])

        if self.system_info['bpm'] == 'auto':
            beat_name = f'{name}_{self.lss.dataset.get_heir().get_bpm()}_{self.lss.dataset.get_heir().get_scale()}.wav'
        else:
            beat_name = f'{name}_{self.system_info["bpm"]}_{self.lss.dataset.get_heir().get_scale()}.wav'

        audio.file.export(name=beat_name,audio=beat)


        logger.info(f'Track exported at: {os.getcwd()}/{beat_name}')
        if len(trackouts.get_data()) > 0:
            os.mkdir('stems')
            os.chdir('stems')
            for i, trackout in enumerate(trackouts.get_items()):
                audio.file.export(name=(f'{name}_{i}.wav'),audio=trackout)
            
            logger.info(f'Trackout included in: {os.getcwd()}/stems')
        os.chdir(self.system_info['basefolder'])

    def get_info():
        ...
 
    def refresh(self, gen_no):

        os.chdir(self.system_info["output_path"])        
        new_dir = f'{self.system_info["preset"]}_{gen_no}'
        logger.info(f'Output folder: {os.getcwd()}')

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            os.chdir(new_dir)
        else:
            cur_time = time.time()
            logger.info(f'Output directory already exists! Creating new unique folder: {new_dir}_{cur_time}')
            os.mkdir(f'{new_dir}_{cur_time}')
            os.chdir(f'{new_dir}_{cur_time}')

        self.system_info['outputdirectory'] = os.getcwd()
        
        logger.info(f'Completed initialization of context for generation no. {gen_no}')
        logger.info(f'Output folder: {os.getcwd()}')

        os.chdir(self.system_info["basefolder"])
        self.lss = None
        self.lss = LSS(self.system_info, gen_no)

        self.beatmaker = None
        self.beatmaker = Ronald(self.system_info)

    def init_log(self):
        formatter = logging.Formatter('%(asctime)s> %(message)s')
        log_file = f'{self.system_info["outputdirectory"]}/log.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return file_handler

    def export_info(self, log_info):
        self.lss.dataset.to_csv(csv_name=f'{self.system_info["output_path"]}/loops.csv')
        logger.removeHandler(log_info)

    def run(self, n_tracks):

        for i in range(n_tracks):
            self.refresh(i)
            log_info = self.init_log()
            self.init_lss(gen_no=i)
            self.beatmaker.info['bar_lenght'] = self.lss.info['bar_lenght']
            self.beatmaker.make_track(self.lss.dataset)
            self.export_section(self.beatmaker.track, i)
            self.export_info(log_info)

            