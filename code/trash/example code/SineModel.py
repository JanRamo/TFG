from locale import normalize
import essentia
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt


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
print(f"Parameters: {params}")

loader = es.MonoLoader(
    filename="/home/pabblo/tfgvco/Kobol_vco_samples/MUESTRA VCO1 KOBOL EXPANDER/Triangular/vco1_5.5_tri.wav", sampleRate=params["sampleRate"]
)
fcut = es.FrameCutter(
    frameSize=params["frameSize"], hopSize=params["hopSize"], startFromZero=True
)
w = es.Windowing(type="hamming", zeroPhase=False)
fft = es.FFT(size=params["frameSize"])
#spectrum = es.Spectrum()
SineModel = es.SineModelAnal(
    sampleRate=params["sampleRate"],
    maxnSines=params["maxnSines"],
    maxFrequency=int(params["sampleRate"]),
    minFrequency= 30,
    magnitudeThreshold=params["magnitudeThreshold"],
    freqDevOffset=params["freqDevOffset"],
    freqDevSlope=params["freqDevSlope"],
)
SineModelSynth = es.SineModelSynth(
    sampleRate=params["sampleRate"],
    fftSize=params["frameSize"],
    hopSize=params["hopSize"],
)
ifft = es.IFFT(size=params["frameSize"], normalize=False)
overl = es.OverlapAdd(frameSize=params["frameSize"], hopSize=params["hopSize"])


audio = loader()
frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]

win = w(frame)
fft_frame = fft(win)
freq, mag, ph = SineModel(fft_frame)
out_frame = SineModelSynth(mag, freq, ph)
ifft_synth = ifft(out_frame)
print(out_frame)

_, ax = plt.subplots(2,1, figsize=(10, 6))
frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)
ax[0].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(fft_frame) + np.finfo(float).eps))
ax[0].set_ylim([-120, -20])
ax[0].set_xlabel("Frequency [Hz]")
ax[0].set_ylabel("Magnitude [dBFS]")
ax[0].set_title("Analyzed Spectrum")

ax[1].semilogx(frequency_stamps, 20.0 * np.log10(np.abs(out_frame) + np.finfo(float).eps))
ax[1].set_ylim([-120, -20])
ax[1].set_xlabel("Frequency [Hz]")
ax[1].set_ylabel("Magnitude [dBFS]")
ax[1].set_title("Synthesized Spectrum")
plt.suptitle("Sine model")
plt.tight_layout()
plt.savefig("Frequency_Magnitude.png")
plt.clf()

# compare peaks
idx_max_in = np.argmax(np.abs(fft_frame))
idx_max_out = np.argmax(np.abs(out_frame))
print(f"Max peak in input frame: {frequency_stamps[idx_max_in]}[Hz]")
print(f"Max peak in output frame: {frequency_stamps[idx_max_out]}[Hz]")


# Audio .wav plot
plt.plot(win)
#plt.xlim([0, 500])
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Time Domain Signal:")
plt.savefig("Windowed_Signal_Time_Domain.png")
plt.clf()

# Audio Synth plot
plt.plot(ifft_synth)
#plt.xlim([0, 500])
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Time Domain Signal:")
plt.savefig("Synth_Signal_Time_Domain.png")
plt.clf()
