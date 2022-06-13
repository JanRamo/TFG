from cProfile import label
from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from os import path
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d



import pathlib
import SineModelAnal, FreqDesvCalc, WaveShaperPlot #, SineModelSynth

#Sample directory
rootDir = '/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO1 KOBOL EXPANDER'
folder = pathlib.Path(rootDir)
count = 0
waveformDir = []
signalFrames = []
#Iterating each subfolder (waveform) from directory
for waveform in folder.iterdir():
    waveformDir = pathlib.Path(waveform)
    print(waveform)
    for sample in waveformDir.iterdir():
      if sample.name.startswith('vco1_0.0') and sample.name.endswith('.wav'):
        sampleDir = pathlib.Path(sample)
        params = {
            "frameSize": 2**15,
            "hopSize": 512,
            "startFromZero": False,
            "sampleRate": 48000,
            "maxnSines": 300,
            "magnitudeThreshold": -80,
            "minSineDur": 0.02,
            "freqDevOffset": 0.1,
            "freqDevSlope": 0.1,
            "maxPeaks": 300,
        }   

        #Load de recording sample given the path 
        loader = es.MonoLoader(
            filename = str(sampleDir), sampleRate=params["sampleRate"]
        )

        w = es.Windowing(type="hamming", zeroPhase=False)
        fft = es.FFT(size=params["frameSize"])
        SineModel = es.SineModelAnal(
            sampleRate=params["sampleRate"],
            maxnSines=params["maxnSines"],
            maxFrequency=int(params["sampleRate"]),
            minFrequency= 10,
            magnitudeThreshold=params["magnitudeThreshold"],
            freqDevOffset=params["freqDevOffset"],
            freqDevSlope=params["freqDevSlope"],
        )
        

        audio = loader()
        frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
        win = w(frame)
        fft_frame = fft(win)
        sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
        fundamentalFrequency = sineFrequencies[0]
        period = 1/fundamentalFrequency
            
        if sample.name.startswith('vco1_0.0'):
            signalFrames.append(frame)
            counter = len(signalFrames)-1

    print("Estos es el counter",counter)
    _, ax = plt.subplots(11,1, figsize=(10, 10))
    frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)
    print(signalFrames)
        
            # for x in signalFrames:
    ax[counter].plot(frame)
    ax[counter].set_xlim([0, 1000000*period])
    ax[counter].set_xlabel("Time [ms]")
    ax[counter].set_ylabel("Amplitude [cm]")
    ax[counter].set_title("Time Signal Spectrum")

    plt.tight_layout()
    plt.savefig('analisis pics/WaveShapers.png')

    count +=1
    print('Analizing', sample.name)
        
            # fft = SineModelSynth.SineModelSynthFunc(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
    print('Total Samples Analized', count)     
        #Initial Parameters for Algorithms
        
