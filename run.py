from lib.calliope import Calliope
import lib.presets as presets

system_info = presets.get_system_config()
presets.load_preset('drill', system_info)

calliope = Calliope(system_info)

calliope.start()