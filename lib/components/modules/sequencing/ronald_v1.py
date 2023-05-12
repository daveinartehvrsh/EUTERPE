from lib.components.abstract.abstract import BeatMaker
from lib.components.datastructs.mixer import Mixer
from lib.components.datastructs.dataset import Dataset
import logging
logger = logging.getLogger('my_logger')

class Ronald(BeatMaker):
    def __init__(self, system_info):
        self.track = Mixer(system_info)

    def make_track(self, dataset: Dataset):
        self.track.fill(dataset)

    def get_info():
        ...