import essentia
import essentia.standard as es
import os.path

# import matplotlib for plotting
import matplotlib.pyplot as plt
import numpy as np
import sys

# algorithm parameters
params = { 'frameSize': pow(2,16), 'hopSize': pow(2,9), 'startFromZero': False, 'sampleRate': 48000,'maxnSines': 10000,'magnitudeThreshold': -2000,'minSineDur': 0.002,'freqDevOffset': 10, 'freqDevSlope': 0.000001}

loader = es.MonoLoader(filename = './audio/sine.wav', sampleRate = params['sampleRate'])
fcut = es.FrameCutter(frameSize = params['frameSize'], hopSize = params['hopSize'], startFromZero =  True)
w = es.Windowing(type='hamming', normalized=False)
fft_audio = es.FFT(size = params['frameSize'])
spectrum = es.Spectrum()
SprModel = es.SprModelAnal(sampleRate = params['sampleRate'], maxnSines = params['maxnSines'], magnitudeThreshold = params['magnitudeThreshold'], freqDevOffset = params['freqDevOffset'], freqDevSlope = params['freqDevSlope'])
ifft = es.IFFT(size = params['frameSize'])
synFFTSize = min(int(params['frameSize']/4), 4*params['hopSize']);  
SprModelSynth = es.SprModelSynth(sampleRate = params['sampleRate'], fftSize = synFFTSize, hopSize = params['hopSize']) 
overl = es.OverlapAdd (frameSize = params['frameSize'], hopSize = params['hopSize'])

audio = loader()
frame = fcut(audio) #audio[0*44100 : 0*44100 + 2048]
win = w(frame)
fft = fft_audio(win)
spec = spectrum(win)

freq, mag, ph, res = SprModel(frame)
fft_frame, fft_sineframe, fft_resframe = SprModelSynth(freq,mag,ph,res)
#ifft_synth = ifft(fft_frame)
tot_frame = fft_frame + fft_sineframe + fft_resframe 
# Audio .wav plot
plt.plot(frame)
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("./pics/Original_Signal_Time_Domain_SPRModel.png") 

# Audio Synth plot
plt.clf()
plt.plot(fft_resframe   )
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("./pics/Synth_Signal_Time_Domain_SPRModel.png")