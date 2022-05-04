import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt

M = 1024

loader = essentia.standard.MonoLoader(filename = './audio/vco1_0.0_saw-sqr+.wav', sampleRate = 44100)
audio = loader()

frame = audio[0*44100 : 0*44100 + 2048]
w = es.Windowing(type='hamming', normalized=False)

spectrum = es.Spectrum() 
spec = spectrum(w(frame))

spectral = es.SpectralPeaks()
freq, mag = spectral(spec)

fft_audio = es.FFT()
fft = fft_audio(frame)



# ------------------ Plotting Values -----------------------
# Audio .wav plot
plt.plot(audio)
plt.xlim([0, 200])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title("Time Domain Signal:")
plt.savefig("Signal_Time_Domain_saw-sqr+.png")
# plt.cla()

# Spectum plot
plt.plot(spec)
plt.xlim([0, 50])
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title("Frequency Domain Signal:")
plt.savefig("Frequency_Time_Domain_saw-sqr+.png")
#plt.savefig("specS.png")

print(spec)
#print(mag)

# Spectral Peaks plot
plt.plot(freq,mag)
plt.xlim([0, 50])
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title("Frequency Domain Signal:")
plt.savefig("Spectral_Peaks_saw-sqr+.png")


print("SprModelAnal")
print("-"*80)
# print(freqe)
# print(magn)

print("FFT")
print("-"*80)
print(fft)
plt.plot(fft)
plt.title("fft:")
plt.savefig("fft2.png")

# plt.plot(spectrum)
# plt.title("The spectrum of a frame:")
# plt.savefig("spec.png")
# # #print(spectrum)
plt.cla()

file = open("Spec_values.txt", "w")
str_spec = repr(spec)
file.write(str_spec)
file.close