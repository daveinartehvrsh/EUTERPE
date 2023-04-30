from configparser import ConfigParser

def get_presets():
    config = ConfigParser()
    config.read('data/config/presets.ini')
    # Get a list of available presets
    presets = config.sections()
    return presets

def get_system_config():
    configur = ConfigParser()
    configur.read('data/config/default.ini')
    system_info = {}
    #   system config load
    system_info['preset name'] = 'default'
    system_info['sr'] = configur.getint('system', 'sr')
    system_info['outputfolder'] = configur.get('system', 'outputfolder')
    system_info['loop_beats'] = configur.getint('system', 'loop_beats')

    #   user defined config
    system_info['bars'] = input('\n| insert lenght of the beat in BARS\n> number of bars: ')
    system_info['BPM'] = input('\n| insert BPM\n> BPM: ')
    if system_info['BPM'] != 'auto':
        system_info['BPM'] = int(system_info['BPM'])
    
    #   tracks config load
    system_info['m_gain'] = configur.getfloat('tracks', 'm_gain')
    system_info['d_gain'] = configur.getfloat('tracks', 'd_gain')
    system_info['b_gain'] = configur.getfloat('tracks', 'b_gain')
    return system_info

def load_preset(selected_preset, system_to_override):
    configur = ConfigParser()
    configur.read('data/config/presets.ini')
    if selected_preset in configur.sections():
        preset_options = configur[selected_preset]
        for option in preset_options:
            system_to_override[option] = preset_options[option]
    else:
        print('invalid preset, back to default')

def main():
    ...
if __name__ == '__main__':
    main()