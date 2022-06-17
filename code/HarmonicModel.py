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
        "maxnSines": 1000,
        "magnitudeThreshold": -90,
        "minSineDur": 0.02,
        "freqDevOffset": 0.1,
        "freqDevSlope": 0.1,
        "maxPeaks": 1000,
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
        nHarmonics = 1000,
        maxPeaks=params["maxPeaks"],
    )
    ifft = es.IFFT(size=params["frameSize"], normalize=False)
    overl = es.OverlapAdd(frameSize=params["frameSize"], hopSize=params["hopSize"])

    audio = loader()
    frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
    win = w(frame)
    try:
        fft_frame = fft(win)
        #Frame Normalization
        fft_frame = fft_frame/np.linalg.norm(fft_frame)
        sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
        fundamentalFrequency = sineFrequencies[0]
        harmonicFrequencies, harmonicMagnitudes, harmonicPhases = HarmonicModel(fft_frame, fundamentalFrequency)
        sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
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
        harmonicMagnitudes = (np.array(harmonicMagnitudesList))
        harmonicPhases = np.array(harmonicPhasesList)
        harmonicPhasesDegree = harmonicPhases*180/np.pi
       
        #Calculating harmonic number from harmonic frequency array
        for x in harmonicFrequencies:
            harmonicNumber = np.round(harmonicFrequencies/fundamentalFrequencyRounded)
        harmonicNumberList = harmonicNumber.tolist()
        #Converting dBv to V
        intHarmonicMagnitudes = harmonicMagnitudes.astype(int)
        vHarmonicMagnitudes = 10**(intHarmonicMagnitudes/20)
        #Calculating THD
        vRMS = vHarmonicMagnitudes/np.sqrt(2)
        thd = np.real(100*(np.sqrt(sum(np.power(vRMS[1:],2))))/vRMS[0])
        print("El THD para la señal",signalName, "es:", np.around(thd, decimals=2,), "%")

        # normalized_v = vHarmonicMagnitudes/np.linalg.norm(vHarmonicMagnitudes)
        # normHarmonicMagnitudes = 20*np.log(normalized_v)
        # normalizedarmonicMagnitudes= harmonicMagnitudes/np.linalg.norm(harmonicMagnitudes)
        # print(normHarmonicMagnitudes)

        #Relation between magnitudes in linear
        harmonicRelationList= []
        for magnitud in vHarmonicMagnitudes:
            harmonicRelationNumber = magnitud/vHarmonicMagnitudes[0]
            harmonicRelationList.append(harmonicRelationNumber)
        # print(harmonicRelationList)

        minHarm = harmonicFrequencies[0]
        maxHarm = max(harmonicFrequencies)
        totHarm = np.count_nonzero(harmonicFrequencies)

        print("Harmonico Menor (Fundamental):", minHarm)
        print("Harmonico Máximo:", maxHarm)
        print("Numero de harmonicos:", totHarm)
        print("\n")
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
        ax[0].set_ylabel("Amplitude [V]")
        ax[0].set_title("Time Signal Spectrum")

        ax[1].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
        ax[1].set_ylim([-100, 0])
        ax[1].set_xlim([10**0, 3.8*10**4])
        ax[1].set_xlabel("Frequency [Hz]")
        ax[1].set_ylabel("Magnitude [dbFS]")
        ax[1].set_title("Frequency Signal Spectrum")
        ax[1].grid(True)
        ax[1].xaxis.grid(True, which='minor')  # minor grid on too

        ax[2].stem(harmonicFrequencies, harmonicMagnitudes, bottom = -100)
        ax[2].set_xlabel("Frequency [Hz]")
        ax[2].set(xscale = 'log')
        ax[2].set_xlim([10**0, 3.8*10**4])
        # ax[2].hlines(params["magnitudeThreshold"], linewidth=2, color='r')
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

        ax[4].bar(harmonicNumber, harmonicRelationList, width=1, edgecolor="white", linewidth=0.7)
        ax[4].set_xlabel("Harmonic Number")
        ax[4].set_xlim([0, 20])
        ax[4].set_ylim([0, 1])
        #ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
        ax[4].set_ylabel("Magnitude [dBFS]")
        # ax.set_ylim([-100, 0])
        ax[4].set_title(str(signalName) + " Harmonics Relation")
        plt.suptitle("HarmonicModelAnalizedSignal: " + str(signalName) + "\nFundamental Frequency: " + str(fundamentalFrequencyRounded) + "Hz")
        plt.tight_layout()
        plt.savefig('analisis pics/HarmonicModelAnalizedSignal_' + str(signalName) + '.png')
        plt.clf()
    except:
        pass


if __name__ == '__main__':
    HarmonicModelAnal()

