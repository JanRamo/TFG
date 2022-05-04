import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt

# # Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
# features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
#                                               rhythmStats=['mean', 'stdev'],
#                                               tonalStats=['mean', 'stdev'])('./audio/vco1_0.0_pul-con.wav')

# See all feature names in the pool in a sorted order
#print(sorted(features.descriptorNames()))
M = 1024

loader = essentia.standard.MonoLoader(filename = './audio/vco1_0.0_pul-con.wav', sampleRate = 44100)
audio = loader()

plt.rcParams['figure.figsize'] = (15, 6)

w = es.Windowing(size = M, type = 'hann')

frame = audio[0*44100 : 0*44100 + 2048]
fft = es.FFT()
audio_fft = fft(frame)
plt.plot(audio_fft)
plt.title("The spectrum of a FFT:")
plt.savefig("fft.png")

spectrum = es.Spectrum(size = M) 
mfcc = es.MFCC()
spec = spectrum(w(frame))
mfcc_bands, mfcc_coeffs = mfcc(spec)

plt.plot(spec)
plt.title("The spectrum of a frame:")
plt.savefig("spec.png")


print("Duration of the audio sample [sec]:")
print(len(audio)/44100.0)

plt.plot(mfcc_bands)
plt.title("Mel band spectral energies of a frame:")
plt.savefig("mfcc.png")

# plot(mfcc_coeffs)
# plt.title("First 13 MFCCs of a frame:")
# show()

# plt.plot(spectrum)
# plt.show()                   # Display the plot
# plt.savefig("plot2.png")







# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(audio)       # Plot the sine of each x point
# plt.show()                   # Display the plot
# plt.savefig("plot1.png")



# print("Filename:", features['metadata.tags.file_name'])
# print("-"*80)
# print("Replay gain:", features['metadata.audio_properties.replay_gain'])
# print("EBU128 integrated loudness:", features['lowlevel.loudness_ebu128.integrated'])
# print("EBU128 loudness range:", features['lowlevel.loudness_ebu128.loudness_range'])
# print("-"*80)
# print("MFCC mean:", features['lowlevel.mfcc.mean'])
# print("-"*80)
# print("BPM:", features['rhythm.bpm'])
# print("Beat positions (sec.)", features['rhythm.beats_position'])
# print("-"*80)
# print("Key/scale estimation (using a profile specifically suited for electronic music):",
#       features['tonal.key_edma.key'], features['tonal.key_edma.scale'])

