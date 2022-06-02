import json
from os import path
import numpy as np
import essentia.standard as es

def DataFromJsonFunc():
    
 
    filename = 'SignalDataa.json'
    SignalData = []
    
    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")
    
    # Read JSON file
    with open(filename) as fp:
        SignalData = json.loads(fp.read())
    
    # Verify existing list
    # print(SignalData[0]['Signal Name'])
    # print(SignalData[0]['Pitch Frequency'])
    # print(SignalData[0]['Harmonics'])
    # print(SignalData[0]['Magnitud'])
    # print(SignalData[0]['Phase'])

    #StrToInt = np.fromstring(SignalData[0]['Harmonics'], dtype=int, sep=' ')
    harmonicFrequencies = np.array(SignalData[0]['Harmonics'])
    harmonicMagnitudes = np.array(SignalData[0]['Magnitud'])
    harmonicPhases = np.array(SignalData[0]['Phase'])
    #convertedArray = harmonicFrequencies.astype(np.float)
    
    print(type(harmonicFrequencies))
    print(harmonicFrequencies)
    #print(np.float32(harmonicFrequencies))
    
    # print(convertedArray)

    sineMagnitudes = harmonicMagnitudes
    #print(harmonicMagnitudes)
    sineFrequencies = harmonicFrequencies
    #print(harmonicFrequencies)
    sinePhases = harmonicPhases
    #print(harmonicPhases)
    # Open the existing json file for loading into a variable
    
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

    SineModelSynth = es.SineModelSynth(
        sampleRate=params["sampleRate"],
        fftSize=params["frameSize"],
        hopSize=params["hopSize"],
    )
    ifft = es.IFFT(size=params["frameSize"], normalize=False)

    #out_frame = SineModelSynth(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
    out_frame = SineModelSynth(sineMagnitudes, sineFrequencies, sinePhases)
    ifft_synth = ifft(out_frame)
    #print(ifft_synth) 


    return
    