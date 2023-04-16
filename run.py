from lib.calliope import Calliope
import lib.presets as presets

system_info = presets.get_system_config()
system_info['preset'] = input('select preset: [ronald, benny, sutoru]')
presets.load_preset(system_info['preset'], system_info)

calliope = Calliope(system_info)

calliope.start()
