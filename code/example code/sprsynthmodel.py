import essentia
import essentia.streaming as es
import os.path

# import matplotlib for plotting
import matplotlib.pyplot as plt
import numpy as np
import sys

# algorithm parameters
params = { 'frameSize': 2048, 'hopSize': 128, 'startFromZero': False, 'sampleRate': 48000,'maxnSines': 100,'magnitudeThreshold': -74,'minSineDur': 0.02,'freqDevOffset': 10, 'freqDevSlope': 0.001}


# loop over all frames
audioout = np.array(0)
counter = 0

# input and output files
path = os.path.dirname(os.path.realpath("C:\\Users\\JAAY\\OneDrive\\Documentos\\REAPER Media\\MUESTRA VCO1 KOBOL EXPANDER"))
#tutorial_dir = os.path.dirname(os.path.realpath(__file__))
inputFilename = os.path.join(path,"Triangular" ,'vco1_5.5_tri.wav')
#outputFilename = os.path.join(tutorial_dir, 'singing-female-out-sprmodel.wav')

out = np.array(0)
loader = es.MonoLoader(filename = './audio/vco1_5_tri.wav', sampleRate =  params['sampleRate'])
pool = essentia.Pool()
fcut = es.FrameCutter(frameSize = params['frameSize'], hopSize = params['hopSize'], startFromZero =  False);
w = es.Windowing(type = "blackmanharris92");
fft = es.FFT(size = params['frameSize']);
smanal = es.SprModelAnal(sampleRate = params['sampleRate'], maxnSines = params['maxnSines'], magnitudeThreshold = params['magnitudeThreshold'], freqDevOffset = params['freqDevOffset'], freqDevSlope = params['freqDevSlope'])
synFFTSize = min(int(params['frameSize']/4), 4*params['hopSize']);  # make sure the FFT size is appropriate
smsyn = es.SprModelSynth(sampleRate = params['sampleRate'], fftSize = synFFTSize, hopSize = params['hopSize'])    



# analysis
loader.audio >> fcut.signal
fcut.frame >> smanal.frame
smanal.magnitudes >> (pool, 'magnitudes')
smanal.frequencies >> (pool, 'frequencies')
smanal.phases >> (pool, 'phases')

# synthesis
smanal.magnitudes >> smsyn.magnitudes
smanal.frequencies >> smsyn.frequencies
smanal.phases >> smsyn.phases    
smanal.res >> smsyn.res

smsyn.frame >> (pool, 'frames')
smsyn.sineframe >> (pool, 'sineframes')
smsyn.resframe >> (pool, 'resframes')

print(fcut.signal)

essentia.run(loader)



#store to file
outaudio = pool['frames'].flatten() 

awrite = es.MonoWriter (filename = './audio/vco1_5_tri_spr.wav', sampleRate =  params['sampleRate'])
outvector = es.VectorInput(outaudio)

outvector.data >> awrite.audio
essentia.run(outvector)

loaderOriginal = es.MonoLoader(filename = './audio/vco1_5_tri.wav', sampleRate = params['sampleRate'])
loaderSynth = es.MonoLoader(filename = './audio/vco1_5_tri_spr.wav', sampleRate = params['sampleRate'])

loaderOriginal.audio_original 
audio_synth = loaderSynth()
# Audio .wav plot
plt.plot(loaderOriginal.audio_original )
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("Original_Signal_Time_Domain_SPRModel.png") 

# Audio Synth plot
plt.clf()
plt.plot(audio_synth)
plt.xlim([0, 500])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("Synth_Signal_Time_Domain_SPRModel.png")