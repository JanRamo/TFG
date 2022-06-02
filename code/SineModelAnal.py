from curses import def_prog_mode
from fileinput import filename
from locale import normalize
from blinker import Signal
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from genericpath import exists
from os import path
from matplotlib.ticker import MaxNLocator

SignalData = []
filename = 'data_vco1_tri.json'
    
    # Write the initial json object (list of dicts)
with open(filename, mode='w') as f:
    json.dump(SignalData, f)

def SineModelAnalFunc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    print(signalName)
   
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 80,
        "magnitudeThreshold": -83,
        "minSineDur": 0.02,
        "freqDevOffset": 1,
        "freqDevSlope": 0.1,
    }
    #print(f"Parameters: {params}")

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
        minFrequency= 30,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset=params["freqDevOffset"],
        freqDevSlope=params["freqDevSlope"],
    )
    HarmonicModel = es.HarmonicModelAnal(sampleRate=params["sampleRate"],
        maxnSines=params["maxnSines"],
        maxFrequency=int(params["sampleRate"]),
        minFrequency= 30,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset=params["freqDevOffset"],
        freqDevSlope=params["freqDevSlope"],
    )

    ifft = es.IFFT(size=params["frameSize"], normalize=False)
    overl = es.OverlapAdd(frameSize=params["frameSize"], hopSize=params["hopSize"])

    audio = loader()
    frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
    win = w(frame)
    fft_frame = fft(win)
    sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
    pitch = sineFrequencies[0]
    harmonicFrequencies, harmonicMagnitudes, harmonicPhases = HarmonicModel(fft_frame, pitch)
    
    SignalData = [
            {
            
                "Signal Name": str(signalName), 
                "Pitch Frequency": str(pitch),
                "Harmonics": str(harmonicFrequencies),
                "Magnitud": str(harmonicMagnitudes),
                "Phase": str(harmonicPhases)   
            }
    ]
    pitch = np.float(pitch)
    period = 1/pitch
    sineFrequenciesList = sineFrequencies.tolist()
    sineMagnitudesList = sineMagnitudes.tolist()
    sinePhasesList = sinePhases.tolist()
    harmonicFrequenciesList = harmonicFrequencies.tolist()
    harmonicMagnitudesList = harmonicMagnitudes.tolist()
    harmonicPhasesList = harmonicPhases.tolist()

    with open(filename) as fp:
        listObj = json.load(fp)
    listObj.append({
                "Signal Name": signalName, 
                "Pitch Frequency": pitch,
                "Sine Frequency": sineFrequenciesList,
                "Sine Magnitud": sineMagnitudesList,
                "Sine Phase": sinePhasesList,
                "Harmonics": harmonicFrequenciesList,
                "Magnitud": harmonicMagnitudesList,
                "Phase": harmonicPhasesList,   
            })
    with open(filename, 'w') as json_file:
        # json.dumps(listObj)
        json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))                

    # SineModelSynth = es.SineModelSynth(
    #     sampleRate=params["sampleRate"],
    #     fftSize=params["frameSize"],
    #     hopSize=params["hopSize"],
    # )
    # ifft = es.IFFT(size=params["frameSize"], normalize=False)

    # #out_frame = SineModelSynth(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
    # out_frame = SineModelSynth(sineMagnitudes, sineFrequencies, sinePhases)
    # ifft_synth = ifft(out_frame)
    # print(ifft_synth)

    # filename = 'data_vco1_tri.json'
    # SignalData = []
    # objectNumber = 3 
    # # Check if file exists
    # if path.isfile(filename) is False:
    #     raise Exception("File not found")
    
    # # Read JSON file
    # with open(filename) as fp:
    #     SignalData = json.loads(fp.read())

    pitchFrequency = np.round(pitch)
    sineFrequencies = np.round(np.array(sineFrequenciesList))
    harmonicFrequencies = np.round(np.array(harmonicFrequenciesList))
    harmonicMagnitudes = np.round(np.array(harmonicMagnitudesList))
    harmonicPhases = np.array(harmonicPhasesList)

    maxHarm = len(sineFrequencies)

    harm = np.empty(maxHarm)
    for j in range (0,maxHarm):
    #p = harmArray.append(j)
        harm[j] = pitchFrequency*j

    #print(harm)
    print(harmonicFrequencies)
    print(harmonicMagnitudes)

# realHarm = []
# for x in sineFrequencies:
#     #print(x)
#     exist = x in harm       
#     #print(exist)   
#     if exist == True:
#         realHarm.append(x)
#         #print(realHarm)
#     if exist == False:
#         print('cañita brava')

    
    for x in harmonicFrequencies:
        harmonicNumber = np.round(harmonicFrequencies/pitchFrequency)

    #Relation between magnitudes
    relationArray= []
    for magnitud in harmonicMagnitudes:
        relationNumber  = harmonicMagnitudes[0]/magnitud
        relationArray.append(relationNumber)

    roundedRelationArray = np.round(relationArray,2)
    print(roundedRelationArray)
    print(harmonicNumber)

    _, ax = plt.subplots(3,1, figsize=(10, 10))
    frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)

    ax[0].plot(frame)
    ax[0].set_xlim([0, 1000000*period])
    ax[0].set_xlabel("Time [s]")
    ax[0].set_ylabel("Amplitude [cm]")
    ax[0].set_title("Time Signal Spectrum")

    ax[1].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
    ax[1].set_ylim([-120, -20])
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude [dBFS]")
    ax[1].set_title("Frequency Signal Spectrum")

# ax[0].set_ylim([-120, -20])
    ax[2].bar(harmonicNumber, harmonicMagnitudes + 100, width=1, edgecolor="white", linewidth=0.7, bottom = -100)
    ax[2].set_xlabel("Harmonic Number")
    ax[2].set_xlim([0, 40])
    #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[2].set_ylabel("Magnitude [dBFS]")
    # ax.set_ylim([-100, 0])
    ax[2].set_title("Harmonics of the Signal")
   
    plt.suptitle("Analized Signal: " + str(signalName) + "\nFundamental Frequency: " + str(pitchFrequency) + "Hz")
    plt.tight_layout()
    plt.savefig('analisis pics/Analized_Signal_' + str(signalName) + '.png')
    plt.clf()


    # compare peaks
    idx_max_in = np.argmax(np.abs(fft_frame)) #frequency_stamps[idx_max_in]
    #print(f"Max peak in input frame: {pitch}[Hz]")

    # Audio .wav plot
    plt.plot(frame)
    #plt.xlim([0, 500])
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Time Domain Signal:")
    plt.savefig("Windowed_Signal_Time_Domain.png")
    plt.clf()
    #print(sinePhases)
    return sineMagnitudes, sineFrequencies, sinePhases
    #return harmonicMagnitudes, harmonicFrequencies, harmonicPhases

if __name__ == '__main__':
    SineModelAnalFunc()