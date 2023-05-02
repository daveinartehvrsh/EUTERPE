from lib.calliope import Calliope
import lib.presets as presets
import time
import logging
import lib.log_info

logger = logging.getLogger('my_logger')

with open('data/welcome.txt') as f:
    print(f.read())
time.sleep(1)

logger.warning('loading deafult configuration...\n')
time.sleep(1)
system_info = presets.get_system_config()

presets.load_preset(system_info['preset'], system_info)

calliope = Calliope(system_info)
n_tracks = int(input('> how many tracks do you want to render?\n! '))
time.sleep(1)
print(f'\n\t\t\t\t!!! STARTING GENERATION of {n_tracks} tracks by {system_info["preset"]}!!!\n')
logger.info(f'generation started at {time.strftime("%H:%M:%S", time.localtime())}')
calliope.run(n_tracks)

