import lib.audio.audio as audio
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
        self.lss = LSS(self.system_info, gen_no)
        self.lss.init_lss()
    
    def export_section(self, section: Mixer, name):
        logger.info(f'      rendering track no. {name}')    
        beat, trackouts = section.render_section(self.lss.dataset.get_heir().get_len())
        os.chdir(self.system_info['outputdirectory'])         
        audio.export(name=(f'{name}.wav'),audio=beat)
        logger.info(f'Track exported at: {os.getcwd()}/{name}.wav | lenght: {len(beat)/self.system_info["sr"]} sec')
        if len(trackouts.get_data()) > 0:
            os.mkdir('stems')
            os.chdir('stems')
            for i, trackout in enumerate(trackouts.get_items()):
                audio.export(name=(f'{name}_{i}.wav'),audio=trackout)
            
            logger.info(f'Mixer exported at {os.getcwd()}\n')
        os.chdir(self.system_info['basefolder'])

    def get_info():
        ...
 
    def refresh(self, gen_no):

        os.chdir(self.system_info["outputfolder"])        
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
        
        logger.info(f'      Completed initialization of context for generation no. {gen_no}')
        logger.info(f'Output folder: {os.getcwd()}')

        os.chdir(self.system_info["basefolder"])

        self.lss = None
        self.lss = LSS(self.system_info, gen_no)

        self.beatmaker = None
        self.beatmaker = Ronald(self.system_info)

    def context_init(self):        
        self.system_info["basefolder"] = os.getcwd()
        os.chdir(self.system_info['outputfolder'])
        gen_dir = f'{time.strftime("%m_%d__%H_%M_%S", time.localtime())}'
        os.mkdir(gen_dir)
        os.chdir(gen_dir)
        self.system_info['outputfolder'] = os.getcwd()
        os.chdir(self.system_info["basefolder"])

    def run(self, n_tracks): 
        formatter = logging.Formatter('%(asctime)s> %(message)s')
        self.context_init()

        for i in range(n_tracks):
            self.refresh(i)
            filename = f'{self.system_info["outputdirectory"]}/generation_{i}.txt'
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.warning(f'STARTING GENERATION OF TRACK {i}')
            logger.info(f'Starting loop selection...')
            self.init_lss(gen_no=i)
            logger.info(f'Starting track creation...')
            self.beatmaker.make_track(self.lss.dataset)
            self.export_section(self.beatmaker.track, i)
            logger.removeHandler(file_handler)