import time 
timer = time.time()
from lib.components.euterpe import Euterpe
import lib.components.presets as presets
import time
import logging
import lib.utils.log_info
import os

def context_init(system_info):
        
    if "output_path" in system_info.keys():
        return
    
    system_info['basefolder'] = os.getcwd()
    output_folder = os.path.join(system_info['user_folder'], 'output')
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    os.chdir(output_folder)
    gen_dir = f'{time.strftime("%d%m_%H%M_%S", time.localtime())}'
    os.mkdir(gen_dir)
    os.chdir(gen_dir)
    system_info['output_path'] = os.getcwd()
    os.chdir(system_info['basefolder'])

logger = logging.getLogger('my_logger')

with open('data/welcome.txt') as f:
    print(f.read())

logger.warning('loading deafult configuration...\n')
system_info = presets.get_system_config()

preset_batch = system_info['preset_batch'].split(',')
logger.warning(f'preset selected: {preset_batch}\n')

print(time.time() - timer, 'seconds to start')
context_init(system_info)
for preset in preset_batch:
    system_info['preset'] = preset
    presets.load_preset(preset, system_info)

    euterpe = Euterpe(system_info)
    time.sleep(1)
    logger.warning('starting generation...\n')
    euterpe.run(n_tracks=int(system_info['n_tracks']))

timer = time.time() - timer
print(f'Done in {float("{:.2f}".format(timer))} seconds')

