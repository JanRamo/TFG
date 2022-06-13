from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from os import path
from matplotlib.ticker import MaxNLocator

SignalData = []
filename = 'json files/HarmonicData_vco1_tri.json'
with open(filename, mode='w') as f:
    json.dump(SignalData, f)
fundamentalFreqDesv = []
#Calculates SineModelAnal, HarmonicModelAnal, Harmonics numbers & relation between them.
def HarmonicModelAnal(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    
    #Initial Parameters for Algorithms
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 300,
        "magnitudeThreshold": -70,
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
    HarmonicModel = es.HarmonicModelAnal(
        sampleRate=params["sampleRate"],
        maxnSines=params["maxnSines"],
        maxFrequency=int(params["sampleRate"]),
        minFrequency= 10,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset=params["freqDevOffset"],
        freqDevSlope=params["freqDevSlope"],
        nHarmonics = 200,
        maxPeaks=300,
    )

    ifft = es.IFFT(size=params["frameSize"], normalize=False)
    overl = es.OverlapAdd(frameSize=params["frameSize"], hopSize=params["hopSize"])

    audio = loader()
    frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
    win = w(frame)
    fft_frame = fft(win)
    sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
    fundamentalFrequency = sineFrequencies[0]

    harmonicFrequencies, harmonicMagnitudes, harmonicPhases = HarmonicModel(fft_frame, fundamentalFrequency)

    fundamentalFrequency = np.float(fundamentalFrequency)
    period = 1/fundamentalFrequency
    phase = np.angle(fft_frame)*180/np.pi
    
    #Converting array to list for JSON file
    #HarmonicModel
    harmonicFrequenciesList = harmonicFrequencies.tolist()
    harmonicMagnitudesList = harmonicMagnitudes.tolist()
    harmonicPhasesList = harmonicPhases.tolist() 

    #Rounding values for an aproximation
    fundamentalFrequencyRounded = np.round(fundamentalFrequency)
    harmonicFrequencies = np.round(np.array(harmonicFrequenciesList))
    harmonicMagnitudes = np.round(np.array(harmonicMagnitudesList))
    harmonicPhases = np.array(harmonicPhasesList)
    harmonicPhasesDegree = harmonicPhases*180/np.pi

    #Calculating harmonic number from harmonic frequency array
    for x in harmonicFrequencies:
        harmonicNumber = np.round(harmonicFrequencies/fundamentalFrequencyRounded)
    harmonicNumberList = harmonicNumber.tolist()
    #Relation between magnitudes
    harmonicRelationList= []
    for magnitud in harmonicMagnitudes:
        harmonicRelationNumber = harmonicMagnitudes[0]/magnitud
        harmonicRelationList.append(harmonicRelationNumber)

    #Creating JSON file 
    with open(filename) as fp:
        listObj = json.load(fp)
    listObj.append({
                "Signal Name": signalName, 
                "Pitch Frequency": fundamentalFrequency,
                "Harmonics": harmonicFrequenciesList,
                "Harmonic Magnitud": harmonicMagnitudesList,
                "Harmonic Phase": harmonicPhasesList,
                "Harmonic Number": harmonicNumberList,
                "Harmonic Relation": harmonicRelationList,
            })
    with open(filename, 'w') as json_file:
        # json.dumps(listObj)
        json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))                
                        
    _, ax = plt.subplots(5,1, figsize=(10, 10))
    frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)

    ax[0].plot(frame)
    ax[0].set_xlim([0, 500000*period])
    ax[0].xaxis.set_major_formatter('{x}x2E5')
    ax[0].set_xlabel("Time [s]")
    ax[0].set_ylabel("Amplitude [cm]")
    ax[0].set_title("Time Signal Spectrum")

    ax[1].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
    ax[1].set_ylim([-100, 0])
    ax[1].set_xlim([10**0, 3.8*10**4])
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude [dBFS]")
    ax[1].set_title("Frequency Signal Spectrum")
    ax[1].grid(True)
    ax[1].xaxis.grid(True, which='minor')  # minor grid on too

    ax[2].stem(harmonicFrequencies, harmonicMagnitudes, bottom = -100)
    ax[2].set_xlabel("Frequency [Hz]")
    ax[2].set(xscale = 'log')
    ax[2].set_xlim([10**0, 3.8*10**4])
    ax[2].grid(True)
    ax[2].xaxis.grid(True, which='minor')  # minor grid on too
    ax[2].set_ylim([-100, 0])
    #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[2].set_ylabel("Magnitude [dBFS]")
    # ax.set_ylim([-100, 0])
    ax[2].set_title("Harmonics Magnitude")

    ax[3].stem(harmonicFrequencies, harmonicPhasesDegree)
    ax[3].set_xlabel("Frequency [Hz]")
    #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[3].set_ylabel("Phase [º]")
    ax[3].set(xscale = "log")
    ax[3].set_xlim([10**0, 3.8*10**4])
    ax[3].set_ylim([-360, 360])
    ax[3].grid(True)
    ax[3].xaxis.grid(True, which='minor')  # minor grid on too
    ax[3].set_title("Harmonics Phase")

    # ax[4].bar(harmonicNumber, harmonicMagnitudes + 100, width=1, edgecolor="white", linewidth=0.7, bottom = -100)
    # ax[4].set_xlabel("Harmonic Number")
    # ax[4].set_xlim([0, 100])
    # ax[4].set_ylim([-100, 0])
    # #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax[4].set_ylabel("Magnitude [dBFS]")
    # # ax.set_ylim([-100, 0])
    # ax[4].set_title("Harmonics of the Signal")

    ax[4].bar(harmonicNumber, harmonicRelationList, width=1, edgecolor="white", linewidth=0.7)
    ax[4].set_xlabel("Harmonic Number")
    ax[4].set_xlim([0, 100])
    ax[4].set_ylim([0, 1])
    #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[4].set_ylabel("Magnitude [dBFS]")
    # ax.set_ylim([-100, 0])
    ax[4].set_title("Harmonics Relation")

    plt.suptitle("HarmonicModelAnalizedSignal: " + str(signalName) + "\nFundamental Frequency: " + str(fundamentalFrequencyRounded) + "Hz")
    plt.tight_layout()
    plt.savefig('analisis pics/HarmonicModelAnalizedSignal_' + str(signalName) + '.png')
    plt.clf()

    return harmonicMagnitudes, harmonicFrequencies, harmonicPhases


if __name__ == '__main__':
    HarmonicModelAnal()

