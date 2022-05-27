from curses import def_prog_mode
from fileinput import filename
from locale import normalize
import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json


def SineModelAnalFunc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    print(sampleDir)
    SignalData = {}
   
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 50,
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

    #print(freq)
    #print(harmonicFrequencies)
    #print(harmonicMagnitudes)

    #dat = np.array([freq, mag, ph])
    
    SignalData = {
        "data": [
            {
                "Signal Name": str(signalName), 
                "Pitch Frequency": str(pitch),
                "Harmonics": str(harmonicFrequencies),
                "Magnitud": str(harmonicMagnitudes),
                "Phase": str(harmonicPhases)
            }
        ]
    }
    s = json.dumps(SignalData, indent=4)
    with open ("SignalData.json","w") as f:
        f.write(s)


    SineModelSynth = es.SineModelSynth(
        sampleRate=params["sampleRate"],
        fftSize=params["frameSize"],
        hopSize=params["hopSize"],
    )
    ifft = es.IFFT(size=params["frameSize"], normalize=False)

    #out_frame = SineModelSynth(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
    out_frame = SineModelSynth(sineMagnitudes, sineFrequencies, sinePhases)
    ifft_synth = ifft(out_frame)

    print(ifft_synth)

    _, ax = plt.subplots(2,1, figsize=(10, 6))
    frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)
    ax[0].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
    ax[0].set_ylim([-120, -20])
    ax[0].set_xlabel("Frequency [Hz]")
    ax[0].set_ylabel("Magnitude [dBFS]")
    ax[0].set_title("Analyzed Spectrum")

    plt.clf()

    # compare peaks
    idx_max_in = np.argmax(np.abs(fft_frame)) #frequency_stamps[idx_max_in]
    print(f"Max peak in input frame: {pitch}[Hz]")

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

def storeData():
    def_prog_mode

if __name__ == '__main__':
    SineModelAnalFunc()
    storeData()