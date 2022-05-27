from locale import normalize
import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
# Import json module
import json

def SineModelSynthFunc(harmonicMagnitudes, harmonicFrequencies, harmonicPhases):
 
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

  print(ifft_synth) 
  
  return ifft_synth

if __name__ == '__main__':
    SineModelSynthFunc()

 # # print(data['data'][0]['Signal Name'])
  # # print(data['data'][0]['Pitch Frequency'])
  # # print(data['data'][0]['Harmonics'])
  # # print(data['data'][0]['Magnitud'])
  # # print(data['data'][0]['Phase'])

  # nameSignal = (data["data"][0]["Signal Name"])
  # pitchFrequency = (data["data"][0]["Pitch Frequency"])

  # Frequencies = (data["data"][0]["Harmonics"])
  # harmonicFrequencies = Frequencies.split()
  # hf = list(map(int, harmonicFrequencies))
  # #harmonicFrequencies = list(map(Frequencies))

  # #print(harmonicFrequencies)
  # #print(*harmonicFrequencies,sep=' ')

  # Magnitudes = (data["data"][0]["Magnitud"])
  # harmonicMagnitudes = Magnitudes.split()
  # Phases = (data['data'][0]["Phase"])
  # harmonicPhases = Phases.split()

  # print(Frequencies)
  # print(harmonicFrequencies)
  # print(hf)
  # # print(Magnitudes)
  # # print(Phases)
  # #out_frame = SineModelSynth(harmonicMagnitudes, harmonicFrequencies, harmonicPhases)
  # #ifft_synth = ifft(out_frame)