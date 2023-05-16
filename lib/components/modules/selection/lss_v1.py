from lib.components.abstract.abstract import AudioSelectionSystem
from lib.components.datastructs.dataset import Dataset
import logging
logger = logging.getLogger('my_logger')

class LSS(AudioSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'name': 'LSS_v1',
            'gen_no': gen_no,
            'BPM': system_info['BPM'],
            'loop_beats': system_info['loop_beats'],
            'sr': system_info['sr'],
            'kits': {
                'drums': {
                    'path': system_info['d_path'],
                    'n_loops': int(system_info['d_n_loops']),
                    'gain': system_info['d_gain'],
                },
                'melody': {
                    'path': system_info['m_path'],
                    'n_loops': int(system_info['m_n_loops']),
                    'gain': system_info['m_gain'],
                },
                'bass': {
                    'path': system_info['b_path'],
                    'n_loops': int(system_info['b_n_loops']),
                    'gain': system_info['b_gain'],
                },
            }
        }
        self.dataset = Dataset(gen_no)
    
    def init_lss(self):
        self.dataset.fill(info=self.info)
        self.dataset.to_csv(csv_name=f'data/loop_count.csv')

    def get_info(self):
        return super().get_info() 
