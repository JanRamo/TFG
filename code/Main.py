import os
import glob, fnmatch
import pathlib
import SineModelAnal
import SineModelSynth

rootDir = '/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO1 KOBOL EXPANDER'
folder = pathlib.Path(rootDir)

waveformDir = []
for waveform in folder.iterdir():
    #print(waveform.name)
    waveformDir = pathlib.Path(waveform)
    #print(files)
    for sample in waveformDir.iterdir():
      if sample.name.endswith('.wav'):
        sampleDir = pathlib.Path(sample)
        #print (sampleDir)
        #print(sample.name)
        harmonicFrequencies, harmonicMagnitudes, harmonicPhases = SineModelAnal.SineModelAnalFunc(sampleDir, sample.name)
        #print(harmonicPhases)
        fft = SineModelSynth.SineModelSynthFunc(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
        #print(harmonicPhases)
        #print(fft)

