from lib.components.abstract.abstract import AudioSelectionSystem
from lib.components.datastructs.dataset import Dataset
import lib.components.presets as presets
import logging
logger = logging.getLogger('my_logger')

class LSS(AudioSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'gen_no': gen_no,
            'bpm': system_info['bpm'],
            'sr': system_info['sr'],
        }

        self.dataset = Dataset(gen_no)
    
    def init_lss(self, system_info):
        self.dataset.fill(info=system_info)
        self.dataset.to_csv(csv_name=f'data/loop_count.csv')

    def get_info(self):
        return super().get_info()
