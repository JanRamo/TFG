from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
import scipy.io.wavfile as wavfile
import numpy
import os.path
from scipy import stats

def SNRCalc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    #Initial Parameters for Algorithms
    params = {
        "frameSize": 2**11,
        "sampleRate": 48000,
        "noiseThreshold": -70,
        "MAAlpha":0.5,
        "MMSEAlpha":0.5,
        "NoiseAlpha": 0.5}
    #Load de recording sample given the path 
    loader = es.MonoLoader(
        filename = str(sampleDir), sampleRate=params["sampleRate"]
    )
    snr = es.SNR(
        sampleRate=params["sampleRate"],
        frameSize=params["frameSize"],
        MAAlpha=params["MAAlpha"],
        MMSEAlpha=params["MMSEAlpha"],
        noiseThreshold=params["noiseThreshold"],
        NoiseAlpha=params["NoiseAlpha"],
        useBroadbadNoiseCorrection=False)
    audio = loader()
    snr_spectral_list = []
    for frame in es.FrameGenerator(
        audio,
        frameSize=params["frameSize"],
        hopSize=params["frameSize"] // 2,):
        # print(frame)
        instantSNR, avgSNR, spectralSNR = snr(frame)
        # print(instantSNR)

    data = wavfile.read(sampleDir)[1]
    singleChannel = data
    try:
      singleChannel = numpy.sum(data, axis=1)
    except:
      # was mono after all
      pass
      
    norm = singleChannel / (max(numpy.amax(singleChannel), -1 * numpy.amin(singleChannel)))
    print(stats.signaltonoise(norm))
if __name__ == '__main__':
    SNRCalc()
