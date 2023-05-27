from configparser import ConfigParser
import os
import logging
logger = logging.getLogger('my_logger')

def get_presets():
    config = ConfigParser()
    config.read('data/generation_config.ini')
    # Get a list of available presets
    presets = config.sections()
    return presets

def get_system_config():
    configur = ConfigParser()
    configur.read('data/system_config.ini')
    system_info = {}
    #   system config load
    system_info['preset name'] = 'default'
    system_info['sr'] = configur.getint('system', 'sr')
    system_info['user_folder'] = configur.get('system', 'user_folder')
    system_info['dataset_path'] = os.path.join(system_info['user_folder'], 'dataset')
    system_info['loop_beats'] = configur.getint('system', 'loop_beats')
    

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
    
    #   tracks config load
    system_info['m_gain'] = configur.getfloat('tracks', 'm_gain')
    system_info['d_gain'] = configur.getfloat('tracks', 'd_gain')
    system_info['b_gain'] = configur.getfloat('tracks', 'b_gain')
    return system_info

def load_preset(selected_preset, system_to_override):
    configur = ConfigParser()
    configur.read('data/generation_config.ini')
    if selected_preset in configur.sections():
        preset_options = configur[selected_preset]
        for option in preset_options:
            system_to_override[option] = preset_options[option]

        system_to_override['d_path'] = os.path.join(system_to_override['dataset_path'], system_to_override['d_path'])
        system_to_override['m_path'] = os.path.join(system_to_override['dataset_path'], system_to_override['m_path'])
        system_to_override['b_path'] = os.path.join(system_to_override['dataset_path'], system_to_override['b_path'])
        logger.info(f'  preset {selected_preset} loaded')
    else:
        print('ERROR: invalid preset, back to default')
        load_preset('default', system_to_override)

def main():
    ...
if __name__ == '__main__':
    main()