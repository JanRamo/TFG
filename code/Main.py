import pathlib
import SineModelAnal, FreqDesvCalc, SNR, SPRModel, HarmonicModel #WaveShaperPlot, SineModelSynth

#Sample directory
rootDir = '/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO1 KOBOL EXPANDER'
folder = pathlib.Path(rootDir)
count = 0
waveformDir = []
#Iterating each subfolder (waveform) from directory
for waveform in folder.iterdir():
    waveformDir = pathlib.Path(waveform)
    # print(waveform)
    for sample in waveformDir.iterdir():
      if sample.name.startswith('vco1') and sample.name.endswith('tri.wav'):
        sampleDir = pathlib.Path(sample)
        # SineModelAnal.SineModelAnal(sampleDir, sample.name)
        # FreqDesvCalc.FreqDesvCalc(sampleDir, sample.name)
        # WaveShaperPlot.WaveShaperPlot(sampleDir, sample.name)
        SNR.SNRCalc(sampleDir, sample.name)
        # SPRModel.SPRModelCalc(sampleDir, sample.name)
        # HarmonicModel.HarmonicModelAnal(sampleDir, sample.name)
        count +=1
        print('Analizing', sample.name)
print('Total Samples Analized', count)     
        