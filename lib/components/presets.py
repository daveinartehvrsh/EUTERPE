from configparser import ConfigParser
import os
import logging
import json
logger = logging.getLogger('my_logger')

def get_system_config():
    configur = ConfigParser()
    configur.read('data/system_config.ini')
    system_info = {}
    #   system config load
    system_info['preset name'] = 'default'
    system_info['sr'] = configur.getint('system', 'sr')
    system_info['user_folder'] = configur.get('system', 'user_folder')
    system_info['loop_beats'] = configur.getint('system', 'loop_lenght')
    #   user defined config
    system_info['n_tracks'] = configur.get('system', 'n_tracks')
    if system_info['n_tracks'] == '?':
        system_info['n_tracks'] = input('> Specify number of tracks\n! ')
    system_info['bars'] = configur.getint('system', 'bars')
    if system_info['bars'] == '?':
        system_info['bars'] = input('> Specify bars lenght of the beat\n! ')
    system_info['bpm'] = configur.get('system', 'BPM')
    if system_info['bpm'] == '?':
        system_info['bpm'] = input('> Insert BPM\n! ')
    if system_info['bpm'] != 'auto':
        system_info['bpm'] = int(system_info['bpm'])
    system_info['preset_batch'] = configur.get('system', 'preset')
    if system_info['preset_batch'] == '?':
        system_info['preset_batch'] = input('> Select preset\n! ')
    
    return system_info

def load(preset_name):
    json_file = open(f'data/presets/{preset_name}.json')
    preset = json.load(json_file)
    json_file.close()
    return preset

def main():
    ...
if __name__ == '__main__':
    main()