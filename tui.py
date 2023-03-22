from calliope import Calliope
import presets

system_info = presets.get_system_config()

calliope = Calliope()

calliope.start(system_info)