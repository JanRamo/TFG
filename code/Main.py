import pathlib
import SineModelAnal #, SineModelSynth

#Sample directory
rootDir = '/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO2 KOBOL EXPANDER'
folder = pathlib.Path(rootDir)
count = 0
waveformDir = []
#Iterating each subfolder (waveform) from directory
for waveform in folder.iterdir():
    waveformDir = pathlib.Path(waveform)
    print(waveform)
    for sample in waveformDir.iterdir():
      if sample.name.startswith('vco2_') and sample.name.endswith('_tri.wav'):
        sampleDir = pathlib.Path(sample)
        #harmonicFrequencies, harmonicMagnitudes, harmonicPhases = SineModelAnal.SineModelAnalFunc(sampleDir, sample.name)
        SineModelAnal.SineModelAnalFunc(sampleDir, sample.name)
        count +=1
        print('Analizing', sample.name)
    
        # fft = SineModelSynth.SineModelSynthFunc(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
print('Total Samples Analized', count)     
        