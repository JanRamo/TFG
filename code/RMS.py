from fileinput import filename
from statistics import mean
import essentia.standard as es
import numpy as np

rmsList = []
def RMSCalc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName

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
    #Load de recording sample given the path 
    loader = es.MonoLoader(
        filename = str(sampleDir), sampleRate=params["sampleRate"]
    )
    rms = es.RMS()
    audio = loader()

    rmsAudio = np.round(rms(audio),5)
    rmsList.append(rmsAudio)
    # avg = sum(rmsList)/len(rmsList)
    print("RMS of the signal:", rmsAudio )
    print("Min RMS:", min(rmsList) )
    print("Max RMS:", max(rmsList) )
    print("Mean RMS:", mean(rmsList) )
    # print("Avg RMS:", avg )

if __name__ == '__main__':
    RMSCalc()