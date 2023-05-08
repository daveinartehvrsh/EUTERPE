import lib.utils.util as util
import lib.audio.audio as audio
import os 

ANALYSIS_DIR = 'data\\01_23'
i = 0

for root, dir, files in os.walk(ANALYSIS_DIR):
    for filename in files:
        if i==0:
            util.loop_to_CSV(filename)
        else:
            util.loop_to_CSV(filename, 'dataset.csv')
        i += 1