import time 
timer = time.time()
from lib.components.euterpe import Euterpe
import lib.components.presets as presets
import time
import logging
import lib.utils.log_info

logger = logging.getLogger('my_logger')

with open('data/welcome.txt') as f:
    print(f.read())

logger.warning('loading deafult configuration...\n')
system_info = presets.get_system_config()

preset_batch = system_info['preset_batch'].split(',')
logger.warning(f'preset selected: {preset_batch}\n')

print(time.time() - timer, 'seconds to start')

for preset in preset_batch:
    system_info['preset'] = preset
    presets.load_preset(preset, system_info)

    euterpe = Euterpe(system_info)
    time.sleep(1)
    logger.warning('starting generation...\n')
    euterpe.run(n_tracks=int(system_info['n_tracks']))

timer = time.time() - timer
print(f'finished in {timer} seconds')

