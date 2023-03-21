from configparser import ConfigParser
from scheme import *

def convert_scheme(str: str):
    scheme = Scheme()
    scheme.load_from_str(str)
    return scheme

def get_system_config(name = 'default.ini'):
    configur = ConfigParser()
    configur.read(name)
    system_info = {}
    system_info['sr'] = configur.getint('system', 'sr')
    system_info['outputfolder'] = configur.get('system', 'outputfolder')
    system_info['loop_rep'] = configur.getint('system', 'loop_rep')
    system_info['steps'] = configur.getint('system', 'steps')
    system_info['m_gain'] = configur.getfloat('tracks', 'm_gain')
    system_info['d_gain'] = configur.getfloat('tracks', 'd_gain')
    system_info['b_gain'] = configur.getfloat('tracks', 'b_gain')
    system_info['m_path'] = configur.get('tracks', 'm_path')
    system_info['d_path'] = configur.get('tracks', 'd_path')
    system_info['b_path'] = configur.get('tracks', 'b_path')
    system_info['m_intensity'] = convert_scheme(configur.get('tracks', 'm_intensity'))
    system_info['d_intensity'] = convert_scheme(configur.get('tracks', 'd_intensity'))
    system_info['b_intensity'] = convert_scheme(configur.get('tracks', 'b_intensity'))
    system_info['m_tune'] = convert_scheme(configur.get('tracks', 'm_tune'))
    system_info['d_tune'] = convert_scheme(configur.get('tracks', 'd_tune'))
    system_info['b_tune'] = convert_scheme(configur.get('tracks', 'b_tune'))
    return system_info

def main():
    ...

if __name__ == '__main__':
    main()