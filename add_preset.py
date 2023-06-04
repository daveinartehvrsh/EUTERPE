import json
import easygui

preset_name = input('preset name: ')
preset = {}

while True:
    channel_name = input('channel name: ')
    preset[channel_name] = {}
    preset[channel_name]['path'] = easygui.diropenbox(title=f'path for {channel_name}')
    preset[channel_name]['n_loops'] = float(input('n_loops: '))
    preset[channel_name]['intensity'] = float(input('intensity: '))
    preset[channel_name]['gain'] = float(input('gain: '))
    preset[channel_name]['tunes'] = float(input('tunes: '))
    if input('add another channel? (y/n) ') == 'n':
        break

json_string = json.dumps(preset, indent=4)
with open(f'data/presets/{preset_name}.json', 'w') as f:
    f.write(json_string)