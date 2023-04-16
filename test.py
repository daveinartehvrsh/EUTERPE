import lib.audio as audio
from lib.classes import Loop

path_1 = 'data\loops/benny\melody\TRKTRN_DST_105_Synth_Loop_Acid_intro_Fmin.wav'
path_2 = 'D:\calliope\dev\data\loops/benny\melody\RKU_LHH2_Rhodes_Vocal_Loop_Tastebud_75_G#min.wav'

data_1, sr_1 = audio.loadLoop(path_1, sr=44100)
data_2, _ = audio.loadLoop(path_2)

loop_1 = Loop(data_1, sr_1, path_1)
loop_2 = Loop(data_2, sr_1, path_2)

pitch_1 = audio.get_tonality(loop_1)
pitch_2 = audio.get_tonality(loop_2)

print(pitch_1)
print(pitch_2)

distance = pitch_1 / pitch_2

print(distance)
