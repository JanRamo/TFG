import essentia
import essentia.standard as es
import os.path

# import matplotlib for plotting
import matplotlib.pyplot as plt
import numpy as np
import sys

# algorithm parameters
params = { 'frameSize': pow(2,10), 'hopSize': pow(2,1), 'startFromZero': False, 'sampleRate': 48000,'maxnSines': 10000,'magnitudeThreshold': -2000,'minSineDur': 0.02,'freqDevOffset': 10, 'freqDevSlope': 0.0001}

loader = es.MonoLoader(filename = './audio/sine.wav', sampleRate = params['sampleRate'])
fcut = es.FrameCutter(frameSize = params['frameSize'], hopSize = params['hopSize'], startFromZero =  True)
w = es.Windowing(type='hann', normalized=False)
fft_audio = es.FFT(size = params['frameSize'])
spectrum = es.Spectrum()
pitch = es.PitchYinFFT()
harmon = es.HarmonicModelAnal(sampleRate = params['sampleRate'], maxnSines = params['maxnSines'], magnitudeThreshold = params['magnitudeThreshold'], freqDevOffset = params['freqDevOffset'], freqDevSlope = params['freqDevSlope'])

audio = loader()
frame = fcut(audio) #audio[0*44100 : 0*44100 + 2048]
win = w(frame)
fft = fft_audio(win)
spec = spectrum(frame)
tunner_freq, conf = pitch (spec)
h_freq, h_mag, h_ph = harmon(fft, tunner_freq)

print(tunner_freq)
print(h_freq)


# Harmonics plot
# plt.clf()
# plt.plot(h_freq)
# #plt.xlim([0, 500])
# plt.xlabel('Frequency')
# plt.ylabel('Amplitude')
# plt.title("./pics/Frequency Domain Signal:")
# plt.savefig("harmonics.png")