from calliope import Calliope
import presets

system_info = presets.get_system_config()
presets.load_preset('drill', system_info)

calliope = Calliope(system_info)

calliope.start()