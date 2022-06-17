from cmath import sqrt
from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from os import path
from matplotlib.ticker import MaxNLocator

#Calculates SineModelAnal, HarmonicModelAnal, Harmonics numbers & relation between them.
def THDCalc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    #Initial Parameters for Algorithms
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 300,
        "magnitudeThreshold": -50,
        "minSineDur": 0.02,
        "freqDevOffset": 0.1,
        "freqDevSlope": 0.1,
        "maxPeaks": 300,
    }
    #print(f"Parameters: {params}")
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
    HarmonicModel = es.HarmonicModelAnal(
        sampleRate=params["sampleRate"],
        maxnSines=params["maxnSines"],
        maxFrequency=int(params["sampleRate"]),
        minFrequency= 10,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset=params["freqDevOffset"],
        freqDevSlope=params["freqDevSlope"],
        nHarmonics = 500,
        maxPeaks=500,
    )

    audio = loader()
    frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
    win = w(frame)
    fft_frame = fft(win)
    fft_frame = fft_frame/np.linalg.norm(fft_frame)
    sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
    fundamentalFrequency = sineFrequencies[0]

    harmonicFrequencies, harmonicMagnitudes, harmonicPhases = HarmonicModel(fft_frame, fundamentalFrequency)

    fundamentalFrequency = np.float(fundamentalFrequency)
    intHarmonicMagnitudes = harmonicMagnitudes.astype(int)
    # print((intHarmonicMagnitudes))

    vHarmonicMagnitudes = 10**(intHarmonicMagnitudes/20)
   
    vRMS = vHarmonicMagnitudes/sqrt(2)
    vHarmRMS = vRMS[1:]
    # print(vRMS)
    thd = np.real(100*(np.sqrt(sum(np.power(vHarmRMS,2))))/vRMS[0])

    # print(vHarmonicMagnitudes)
    print("El THD para la señal",signalName, "es:", np.around(thd, decimals=2,), "%")

if __name__ == '__main__':
    THDCalc()

