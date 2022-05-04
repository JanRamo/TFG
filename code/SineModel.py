import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt

params = { 'frameSize': 128, 'hopSize': 512, 'startFromZero': False, 'sampleRate': 48000,'maxnSines': 10000,'magnitudeThreshold': -100,'minSineDur': 0.02,'freqDevOffset': 10, 'freqDevSlope': 0.001}

loader = es.MonoLoader(filename = './audio/vco1_5_tri.wav', sampleRate = params['sampleRate'])
fcut = es.FrameCutter(frameSize = params['frameSize'], hopSize = params['hopSize'], startFromZero =  True)
w = es.Windowing(type='hamming', normalized=False)
fft_audio = es.FFT(size = params['frameSize'])
spectrum = es.Spectrum()
SineModel = es.SineModelAnal(sampleRate = params['sampleRate'], maxnSines = params['maxnSines'], magnitudeThreshold = params['magnitudeThreshold'], freqDevOffset = params['freqDevOffset'], freqDevSlope = params['freqDevSlope'])
SineModelSynth = es.SineModelSynth(sampleRate = params['sampleRate'], fftSize = params['frameSize'], hopSize = params['hopSize'])
ifft = es.IFFT(size = params['frameSize'])
overl = es.OverlapAdd (frameSize = params['frameSize'], hopSize = params['hopSize'])


audio = loader()
frame = fcut(audio) #audio[0*44100 : 0*44100 + 2048]
win = w(frame)
fft = fft_audio(win)
spec = spectrum(win)
freq, mag, ph = SineModel(fft)

# print(freq)
# print(mag)
# print(ph)

fft_frame = SineModelSynth(freq,mag,ph)
ifft_synth = ifft(fft_frame)

print(fft_frame)

# Audio .wav plot
plt.plot(frame)
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("Original_Signal_Time_Domain.png") 

# Audio Synth plot
plt.clf()
plt.plot(ifft_synth)
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("Synth_Signal_Time_Domain.png")




