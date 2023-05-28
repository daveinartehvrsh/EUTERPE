from lib.components.abstract.abstract import AudioSelectionSystem
from lib.components.datastructs.dataset import Dataset
import lib.components.presets as presets
import logging
logger = logging.getLogger('my_logger')

class LSS(AudioSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'name': 'LSS_v1',
            'gen_no': gen_no,
            'bpm': system_info['bpm'],
            'loop_beats': system_info['loop_beats'],
            'sr': system_info['sr'],
            'kits': presets.load(system_info['preset'])
        }

        if 'bar_lenght' in system_info:
            self.info['bar_lenght'] = system_info['bar_lenght']

        self.dataset = Dataset(gen_no)
    
    def init_lss(self):
        self.dataset.fill(info=self.info)
        self.dataset.to_csv(csv_name=f'data/loop_count.csv')

    def get_info(self):
        return super().get_info()
