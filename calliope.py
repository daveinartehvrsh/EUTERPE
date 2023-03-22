from classes import *
import audio
import presets
from rich.progress import track
import analyze
import librosa

class Calliope(Algorithm):

    def __init__(self):
        self.datasets = {}
        self.sections = {}
        self.tracks = {}
        self.intensity_schemes = []
    
    def create_loopkit(self, name='loopkit', loopkit_preset=None):
        loopkit = Loopkit(name)
        loopkit.fill(loopkit_preset)
        return loopkit

    def create_dataset(self, name, system_info):
        dataset = Dataset()

        drum_info = {'path': system_info['d_path'], 'tune_scheme': system_info['d_tune']}
        drum_loopkit = self.create_loopkit(name='drums', loopkit_preset=drum_info)

        melody_info = {'path': system_info['m_path'],'intensity_scheme': system_info['m_intensity'], 'tune_scheme': system_info['m_tune']}
        melody_loopkit = self.create_loopkit(name='melody', loopkit_preset=melody_info)

        bass_info = {'path': system_info['b_path'],'intensity_scheme': system_info['b_intensity'], 'tune_scheme': system_info['b_tune']}
        bass_loopkit = self.create_loopkit(name='bass', loopkit_preset=bass_info)
    
        dataset.addItem(drum_loopkit)
        dataset.addItem(melody_loopkit)
        dataset.addItem(bass_loopkit)
        
        self.datasets[name] = dataset
    
    def create_loopseq(self, loopkit, intensity_scheme, repetitions):
        loopseq = LoopSeq()
        loopseq.setName(loopkit.getName())
        loopseq.setIntensityScheme(intensity_scheme)
        loops = list(loopkit.getItems())
        loopseq.fill(loopkit=loops, repetitions = repetitions)
        return loopseq
        
    def create_section(self, dataset: Dataset, name, system_info):
        section = Section()

        drum_info = {'intensity_scheme': system_info['d_intensity']}
        drum_seq = self.create_loopseq(dataset.data[0].data, drum_info['intensity_scheme'], system_info['loop_rep'])

        melody_info = {'intensity_scheme': system_info['m_intensity']}
        melody_seq = self.create_loopseq(dataset.data[1].data, melody_info['intensity_scheme'], system_info['loop_rep'])

        bass_info = {'intensity_scheme': system_info['b_intensity']}
        bass_seq = self.create_loopseq(dataset.data[2].data, bass_info['intensity_scheme'], system_info['loop_rep'])

        section.addItem(drum_seq)
        section.addItem(melody_seq)
        section.addItem(bass_seq)

        section.set_bar_lenght()
        section.stretch_section()
        self.sections[name] = section

    def export_section(self, section: Section, name):
        beat, trackouts = section.render_section()
        cwd = os.getcwd()
        out = 'data/out'
        os.chdir(out)
        audio.export(name=(f'track{name}.wav'),audio=beat)
        section.getInfo()
        os.chdir(cwd)
    
    def analyze(self, system_info):
        
        ref, _ = librosa.load(system_info['reference'], sr=system_info['sr'])
        dir = 'C:/Users/david/Documents/CALLIOPE/alpha/data/out'
        sr=system_info['sr']

        for filename in os.listdir(dir):

            f = os.path.join(dir, filename)
            beat, _ = librosa.load(f, sr=sr)
            mfccScore = analyze.mfccDTWScore(beat, ref, sr)
            chromaScore = analyze.chromaDTWScore(beat, ref, sr)
            loopinfo = [mfccScore, chromaScore]

    def getInfo():
        ...

    def stop(self):    
        ...
    
    def start(self, system_info): 
        for i in range(system_info['steps']):
            self.create_dataset(i, system_info=system_info)
            self.create_section(self.datasets[i], i, system_info)
            self.export_section(self.sections[i], i)
            #self.analyze(system_info)
        
def main():
    system_info = presets.get_system_config()    
    calliope = Calliope()
    calliope.start(system_info)

if __name__ == '__main__':
    main()