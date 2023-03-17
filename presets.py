from configparser import ConfigParser

def get_default_config():
    configur = ConfigParser()
    configur.read('config.ini')
    system_info = {}
    system_info['sr'] = configur.getint('system_default', 'sr')
    system_info['n_tracks'] = configur.getint('system_default', 'n_tracks')
    system_info['default_dataset'] = configur.get('system_default', 'default_dataset')
    system_info['default_track'] = configur.get('system_default', 'default_track')
    system_info['repetitions'] = configur.getint('system_default', 'repetitions')
    return system_info
    

def get_default_dataset(name):
    configur = ConfigParser()
    configur.read('config.ini')
    loopkit_names = configur.get(name, 'loopkits')
    dataset_preset = {} 
    for loopkit_name in loopkit_names.split(', '):
        loopkit_preset = {}
        loopkit_preset['path'] = configur.get(loopkit_name, 'path')
        tune_scheme = configur.get(loopkit_name, 'tune_scheme')
        loopkit_preset['tune_scheme'] = tune_scheme.split(', ')
        dataset_preset[loopkit_name] = loopkit_preset
    return dataset_preset

def get_schemes(name):
    configur = ConfigParser()
    configur.read('config.ini')
    scheme_names = configur.get(name, 'intensity_schemes')
    schemes = []
    for item in scheme_names.split(', '):
        schemes.append(configur.get('schemes', item))
    return schemes

def main():
    ...

if __name__ == '__main__':
    main()