import os
import glob, fnmatch
import pathlib
import SineModelAnal, SineModelSynth, DataFromJson


rootDir = '/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO2 KOBOL EXPANDER'
folder = pathlib.Path(rootDir)
count = 0
waveformDir = []
for waveform in folder.iterdir():
    #print(waveform.name)
    waveformDir = pathlib.Path(waveform)
    #print(files)
    for sample in waveformDir.iterdir():
      if sample.name.startswith('vco2_') and sample.name.endswith('_sqr.wav'):
        sampleDir = pathlib.Path(sample)
        #harmonicFrequencies, harmonicMagnitudes, harmonicPhases = SineModelAnal.SineModelAnalFunc(sampleDir, sample.name)
        SineModelAnal.SineModelAnalFunc(sampleDir, sample.name)
        count +=1
        print('Samples Analized', count)
        # fft = SineModelSynth.SineModelSynthFunc(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
     
        
#DataFromJson.DataFromJsonFunc()