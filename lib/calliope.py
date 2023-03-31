from lib.classes import *
import lib.audio as audio
import lib.presets as presets
import lib.analyze as analyze
import librosa
from lib.scheme_utils import *

class LOS_v1(LoopSelectionSystem):

    def __init__(self, system_info):

        self.drum_kit = {
            'path': system_info['d_path'],
            'n_loops': system_info['d_n_loops'],
        }
        self.melody_kit = {
            'path': system_info['m_path'],
            'n_loops': system_info['m_n_loops'],
        }
        self.bass_kit = {
            'path': system_info['b_path'],
            'n_loops': system_info['b_n_loops'],
        }

    def create_drum_loopkit(self, name='drums'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.drum_kit['path'], n_loops = self.drum_kit['n_loops'])
        return loopkit
    
    def create_melody_loopkit(self, name='melody'):
        loopkit = Loopkit(name)       
        loopkit.fill(path = self.melody_kit['path'], n_loops = self.melody_kit['n_loops'])
        return loopkit
    
    def create_bass_loopkit(self, name='bass'):
        loopkit = Loopkit(name)
        loopkit.fill(path = self.bass_kit['path'], n_loops = self.bass_kit['n_loops'])
        return loopkit

    def create_dataset(self, name):
        dataset = Dataset()

        drum_loopkit = self.create_drum_loopkit()
        melody_loopkit = self.create_melody_loopkit()
        bass_loopkit = self.create_bass_loopkit()
    
        dataset.addItem(drum_loopkit)
        dataset.addItem(melody_loopkit)
        dataset.addItem(bass_loopkit)
        
        return dataset

    def getInfo(self):
        return super().getInfo() 
    
class Calliope(Algorithm):

    def __init__(self, system_info):
        self.system_info = system_info
        self.los = LOS_v1(system_info)
        self.datasets = {}
        self.sections = {}
        self.tracks = ScoreMap()
        self.intensity_schemes = []
    
    def render_drum_intensity(self):
        d_intensity = self.system_info['d_intensity'].convert_to_len(self.system_info['loop_rep'])
        out = random_round(d_intensity)
        print(out)
        return out
    
    def render_melody_tune(self):
        m_intensity = self.system_info['m_intensity'].convert_to_len(self.system_info['loop_rep'])
        m_intensity = random_round(m_intensity)
        out = []
        for i in m_intensity:
            out.append(i*-12)
        print(out)
        return out
    
    def render_melody_intensity(self):
        m_intensity = self.system_info['m_intensity'].convert_to_len(self.system_info['loop_rep'])
        out = np.ones(len(m_intensity))
        return out
    
    def render_bass_intensity(self):
        b_intensity = self.system_info['b_intensity'].convert_to_len(self.system_info['loop_rep'])
        out = random_round(b_intensity)
        print(out)
        return out
    
    def create_dataset(self, name):       
        self.datasets[name] = self.los.create_dataset(name)
    
    def create_drum_loopseq(self, loopkit, repetitions):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        loopseq.fill(loopkit=loops, repetitions = repetitions, gain=self.system_info['d_gain'])
        return loopseq
    
    def create_melody_loopseq(self, loopkit, repetitions):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        tune_scheme = self.render_melody_tune()
        loopseq.fill(loopkit=loops, repetitions = repetitions, gain=self.system_info['m_gain'], tune_scheme=tune_scheme)
        return loopseq
    
    def create_bass_loopseq(self, loopkit, repetitions):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loops = list(loopkit.getItems())
        loopseq.fill(loopkit=loops, repetitions = repetitions, gain=self.system_info['b_gain'])
        return loopseq

    def create_section(self, dataset: Dataset, name):
        section = Section()
        rep = self.system_info['loop_rep']
        drum_seq = self.create_drum_loopseq(dataset.data[0].data, rep)
        melody_seq = self.create_melody_loopseq(dataset.data[1].data, rep)
        bass_seq = self.create_bass_loopseq(dataset.data[2].data, rep)

        section.addItem(drum_seq)
        section.addItem(melody_seq)
        section.addItem(bass_seq)

        section.set_bar_lenght()
        section.stretch_section()
        self.sections[name] = section

    def export_section(self, section: Section, name):
        intensity_schemes = [self.render_drum_intensity(),
                            self.render_melody_intensity(),
                            self.render_bass_intensity()]
        beat, trackouts = section.render_section(intensity_schemes)
        cwd = os.getcwd()
        out = 'data/out'
        os.chdir(out)
        audio.export(name=(f'track{name}.wav'),audio=beat)
        os.chdir(cwd)
    
    def add_track(self, section: Section, name):
        intensity_schemes = [self.render_drum_intensity(),
                            self.render_melody_intensity(),
                            self.render_bass_intensity()]
        beat , _ = section.render_section(intensity_schemes)
        self.tracks.addItem(ScoreVector(name=name, data=self.analyze(beat)))
               
    def analyze(self, beat):
        sr=self.system_info['sr']
        
        ref, _ = librosa.load(self.system_info['reference'], sr=sr)
        
        mfccScore = analyze.mfccDTWScore(beat, ref, sr)
        chromaScore = analyze.chromaDTWScore(beat, ref, sr)

        mfccDTW = Score('mfccDTW', mfccScore)
        chromaDTW = Score('chromaDTW', chromaScore)
        
        vector = [mfccDTW, chromaDTW]

        return vector

    def getInfo():
        ...

    def stop(self):    
        ...
    
    def start(self): 
        for i in range(self.system_info['steps']):
            self.create_dataset(i)
            self.create_section(self.datasets[i], i)
            #self.add_track(self.sections[i], i)
            self.export_section(self.sections[i], i)
        
def main():
    system_info = presets.get_system_config()    
    calliope = Calliope(system_info)
    calliope.start()
    calliope.tracks.getInfo()

if __name__ == '__main__':
    main()