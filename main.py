from lib.components.euterpe import Euterpe
import lib.components.presets as presets
import time
import logging
import lib.utils.log_info

logger = logging.getLogger('my_logger')

with open('data/welcome.txt') as f:
    print(f.read())
time.sleep(1)

logger.warning('loading deafult configuration...\n')
time.sleep(1)
system_info = presets.get_system_config()

presets.load_preset(system_info['preset'], system_info)

euterpe = Euterpe(system_info)
n_tracks = int(input('> how many tracks do you want to render?\n! '))
time.sleep(1)
logger.warning('starting generation...\n')
euterpe.run(n_tracks)

