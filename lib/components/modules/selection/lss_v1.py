from lib.components.abstract.abstract import AudioSelectionSystem
from lib.components.datastructs.dataset import Dataset
import logging
logger = logging.getLogger('my_logger')

class LSS(AudioSelectionSystem):

    def __init__(self, system_info, gen_no):
        self.info = {
            'name': 'LSS_v1',
            'gen_no': gen_no
        }
        self.dataset = Dataset(system_info, gen_no)
    
    def init_lss(self):
        self.dataset.fill()

    def get_info(self):
        return super().get_info() 
