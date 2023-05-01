from lib.calliope import Calliope
import lib.presets as presets
import time

with open('data/welcome.txt') as f:
    print(f.read())
time.sleep(1)

print('\n| loading deafult configuration...\n')
time.sleep(1)
system_info = presets.get_system_config()

presets.load_preset(system_info['preset'], system_info)

calliope = Calliope(system_info)
n_tracks = int(input('\n| how many tracks do you want to render?\n> '))
time.sleep(1)
print(f'\n\t\t\t\t!!! STARTING GENERATION of {n_tracks} tracks by {system_info["preset"]}!!!\n')
calliope.run(n_tracks, log=True)

