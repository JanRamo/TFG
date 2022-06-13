from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from os import path
from matplotlib.ticker import MaxNLocator

SignalData = []
filename = 'json files/data_vco1_pul-con.json'
with open(filename, mode='w') as f:
    json.dump(SignalData, f)
fundamentalFreqDesv = []
#Calculates SineModelAnal, HarmonicModelAnal, Harmonics numbers & relation between them.
def SPRModelCalc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    
    #Initial Parameters for Algorithms
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 600,
        "magnitudeThreshold": -80,
        "minSineDur": 0.02,
        "freqDevOffset": 0.1,
        "freqDevSlope": 0.1,
        "maxPeaks": 600,
    }
    #print(f"Parameters: {params}")

    #Load de recording sample given the path 
    loader = es.MonoLoader(
        filename = str(sampleDir), sampleRate=params["sampleRate"]
    )
    
    fcut = es.FrameCutter(
        frameSize=params["frameSize"], hopSize=params["hopSize"], startFromZero=True
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
    SprModel = es.SprModelAnal(
        sampleRate=params["sampleRate"],
        maxnSines=params["maxnSines"],
        maxPeaks=params["maxnSines"],
        maxFrequency=int(params["sampleRate"]),
        minFrequency= 10,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset= 1,
        freqDevSlope=params["freqDevSlope"],
    )  
    AudioWriter = es.AudioWriter(filename = "SNR", sampleRate=params["sampleRate"])

    ifft = es.IFFT(size=params["frameSize"], normalize=False)
    overl = es.OverlapAdd(frameSize=params["frameSize"], hopSize=params["hopSize"])

    audio = loader()
    frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
    win = w(frame)
    fft_frame = fft(win)
    sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
    fundamentalFrequency = sineFrequencies[0]

    SprFrequencies, SprMagnitudes, SprPhases, SprRes = SprModel(frame)
    SprMagnitudesLineal = 10**(SprMagnitudes/20.0)

    SprMagnitudesNorm =  SprMagnitudes/np.linalg.norm(SprMagnitudes)

    #Calculating values from fft frame
    fundamentalFrequency = np.float(fundamentalFrequency)
    period = 1/fundamentalFrequency
    phase = np.angle(fft_frame)*180/np.pi

    #SprModel
    SprFrequenciesList = SprFrequencies.tolist()
    SprMagnitudesList = SprMagnitudes.tolist()
    SprPhasesList = SprPhases.tolist()
    SprResList = SprRes.tolist()

    #Creating JSON file 
    with open(filename) as fp:
        listObj = json.load(fp)
    listObj.append({
                "Signal Name": signalName, 
                "Pitch Frequency": fundamentalFrequency,

            })
    with open(filename, 'w') as json_file:
        # json.dumps(listObj)
        json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))                

    SPRModelSynth = es.SprModelSynth(
        sampleRate=params["sampleRate"],
        fftSize=params["frameSize"],
        hopSize=params["hopSize"],
    )
    ifft = es.IFFT(size=params["frameSize"], normalize=False)

    SPRoutframe, SPRoutSineFrame, SPRoutRes = SPRModelSynth(SprMagnitudes, SprFrequencies, SprPhases, SprRes)
    SPRwin = w(SPRoutRes)
    fftSPRFrame = fft(SPRwin)
    ifft_synth = ifft(fftSPRFrame)
    AudioWriter(ifft_synth)
    print(len(fft_frame))
    print(len(fftSPRFrame))

    _, ax = plt.subplots(2,1, figsize=(10, 6))
    frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)
    ax[0].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
    ax[0].set_ylim([-120, -20])
    ax[0].set_xlabel("Frequency [Hz]")
    ax[0].set_ylabel("Magnitude [dBFS]")
    ax[0].set_title("Analyzed Spectrum")

    ax[1].semilogx(20.0 * np.log10(np.abs(ifft_synth)))
    ax[1].set_ylim([-300, -20])
    ax[1].set_xlim([10**0, 3.8*10**4])
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude [dBFS]")
    ax[1].set_title("Synthesized Spectrum")

    plt.suptitle("Analized Signal: " + str(signalName) + "\nFundamental Frequency: " + str(fundamentalFrequency) + "Hz")
    plt.tight_layout()
    plt.savefig('analisis pics/SPRAnalizedSignal_' + str(signalName) + '.png')
    plt.clf()

if __name__ == '__main__':
    SPRModelCalc()
