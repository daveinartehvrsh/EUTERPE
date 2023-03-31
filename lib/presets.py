from configparser import ConfigParser
from lib.datastructs import Scheme

def get_presets():
    config = ConfigParser()
    config.read('data/presets.ini')
    # Get a list of available presets
    presets = config.sections()
    return presets

def convert_scheme(str: str):
    scheme = Scheme()
    scheme.load_from_str(str)
    return scheme

def get_system_config(name = 'data/default.ini'):
    configur = ConfigParser()
    configur.read(name)
    system_info = {}
    if name=='data/default.ini':
        system_info['preset name'] = 'default'
        system_info['sr'] = configur.getint('system', 'sr')
        system_info['outputfolder'] = configur.get('system', 'outputfolder')
        system_info['loop_rep'] = configur.getint('system', 'loop_rep')
        system_info['steps'] = configur.getint('system', 'steps')
        system_info['reference'] = configur.get('system', 'reference')
        system_info['m_gain'] = configur.getfloat('tracks', 'm_gain')
        system_info['d_gain'] = configur.getfloat('tracks', 'd_gain')
        system_info['b_gain'] = configur.getfloat('tracks', 'b_gain')
        system_info['m_path'] = configur.get('tracks', 'm_path')
        system_info['d_path'] = configur.get('tracks', 'd_path')
        system_info['b_path'] = configur.get('tracks', 'b_path')
        system_info['m_intensity'] = convert_scheme(configur.get('tracks', 'm_intensity'))
        system_info['d_intensity'] = convert_scheme(configur.get('tracks', 'd_intensity'))
        system_info['b_intensity'] = convert_scheme(configur.get('tracks', 'b_intensity'))
        system_info['d_n_loops'] = configur.getint('tracks', 'd_n_loops')
        system_info['m_n_loops'] = configur.getint('tracks', 'm_n_loops')
        system_info['b_n_loops'] = configur.getint('tracks', 'b_n_loops')
    return system_info

def load_preset(selected_preset, system_to_override):
    configur = ConfigParser()
    configur.read('data/presets.ini')
    if selected_preset in configur.sections():
        preset_options = configur[selected_preset]
        for option in preset_options:
            system_to_override[option] = preset_options[option]
    else:
        print('invalid preset, back to default')

def main():
    system_info = get_system_config()
    system_info = load_preset()

if __name__ == '__main__':
    main()