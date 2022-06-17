from cProfile import label
from fileinput import filename
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt
import json
from os import path
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d

fundamentalFreqDesv = []

def FreqDesvCalc(sampleDir, signalName):
    sampleDir = sampleDir
    signalName = signalName
    
    #Initial Parameters for Algorithms
    params = {
        "frameSize": 2**15,
        "hopSize": 512,
        "startFromZero": False,
        "sampleRate": 48000,
        "maxnSines": 300,
        "magnitudeThreshold": -80,
        "minSineDur": 0.02,
        "freqDevOffset": 0.1,
        "freqDevSlope": 0.1,
        "maxPeaks": 300,
    }

    #Load de recording sample given the path 
    loader = es.MonoLoader(
        filename = str(sampleDir), sampleRate=params["sampleRate"]
    )

    w = es.Windowing(type="hamming", zeroPhase=False)
    fft = es.FFT(size=params["frameSize"])
    SineModel = es.SineModelAnal(
        sampleRate=params["sampleRate"],
        maxnSines=params["maxnSines"],
        maxFrequency=int(params["sampleRate"]),
        minFrequency= 10,
        magnitudeThreshold=params["magnitudeThreshold"],
        freqDevOffset=params["freqDevOffset"],
        freqDevSlope=params["freqDevSlope"],
    )

    try:
        audio = loader()
        frame = audio[1*params["sampleRate"] : 1*params["sampleRate"] + params["frameSize"]] #fcut(audio)  # audio[0*44100 : 0*44100 + 2048]
        win = w(frame)
        fft_frame = fft(win)
        sineFrequencies, sineMagnitudes, sinePhases = SineModel(fft_frame)
        fundamentalFrequency = sineFrequencies[0]
        if signalName.startswith('vco2_10.0'):
            fundamentalFreqDesv.append(fundamentalFrequency)
    
    except Exception:
        pass

    #Desviation Freq Calculation
    # print(fundamentalFreqDesv)
    # print(np.mean(fundamentalFreqDesv))
    # print(np.std(fundamentalFreqDesv))

    refFreq = np.array([20, 30, 40, 60, 80, 120, 160, 240, 320, 480, 640, 960, 1280, 1920, 2560, 3840, 5120, 7680, 10240, 15360, 20480])
    
    vco1mean = np.array([19.610476, 27.962677, 43.04703, 55.860424, 78.81932, 110.89857, 188.18004, 224.63579, 315.3355, 444.6008, 697.04803, 896.05646, 1250.0177, 1771.4794, 2516.8354,3560.9685,5008.7983,7196.765,10001.7295,14143.844,20326.809 ])
    vco1Dev = np.array([0.14147215, 0.46101436, 0.664842, 1.3567688, 1.3941922, 1.9961374, 2.32328, 3.8696914, 5.230056, 7.848492, 7.39935, 15.242393, 18.6884, 31.79214, 38.244366, 63.630047, 67.59781, 116.49191, 146.785, 277.34982, 336.76917])
    vco1error =  np.subtract(refFreq, vco1mean)
    vco1RelDev = (np.array(vco1Dev)/np.array(vco1mean))

    vco2mean = np.array([19.961159, 28.364641,40.50251, 57.256012, 80.44317, 114.43206, 159.13301, 230.01718, 325.49472, 455.2111, 645.3108, 917.4182, 1281.8708, 1814.9803, 2600.8098, 3682.38, 5215.7056, 7346.373, 10343.904, 14476.79, 20693.67])
    vco2Dev = np.array([0.07818999, 0.5718593,0.7847117, 1.1748385, 1.3437734, 2.0239651, 1.314794, 3.800631, 3.8446052, 6.1176195, 10.5511, 10.157912, 24.992046, 33.49677, 35.731564, 57.436802, 89.59915, 147.73831, 212.94382, 305.27286, 298.6616 ])
    vco2RelDev = (np.array(vco2Dev)/np.array(vco2mean))

    plt.errorbar(refFreq, vco1RelDev,  linestyle='none', marker='.', label = 'vco1')
    plt.errorbar(refFreq, vco2RelDev,  linestyle='none', marker='x', label = 'vco2')
    for xc in refFreq:
        plt.axvline(x=xc, color='r', linewidth=0.5)

    plt.xscale('log')
    plt.grid(True)
    plt.grid(True, which='minor')  # minor grid on too
    plt.xlabel('Frequencies [Hz]')
    plt.ylabel('Std Relative Deviation')
    plt.title('Desviación Standard Relativa por Frecuencia Sampleada')
    default_x_ticks = range(len(refFreq))
    
    plt.tick_params(axis='x', labelsize=5)
    plt.xticks(refFreq, refFreq)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('analisis pics/FreqDesv.png')
    plt.clf()

if __name__ == '__main__':
    FreqDesvCalc()

[19.564737, 19.653126, 19.795874, 19.483877, 19.48455, 19.644478, 19.910229, 19.483128, 19.72121, 19.484585, 19.489422]
19.610476
0.14147215

[27.983925, 27.866358, 28.703331, 27.607704, 27.48577, 27.738945, 28.119427, 27.872616, 28.47373, 27.139236, 28.598417]
27.962677
0.46101436

[39.321182, 39.52381, 39.18581, 40.330853, 39.33203, 76.730736, 38.97261, 39.520153, 39.497894, 40.719837, 40.382385]
43.04703
10.664842

[54.603004, 57.26875, 56.777924, 55.296104, 54.37398, 54.419273, 54.573174, 56.75667, 56.02741, 58.8036, 55.564754]
55.860424
1.3567688

[77.72896, 77.41196, 78.83255, 78.42334, 79.72799, 78.17497, 80.506004, 77.69301, 81.926125, 77.76832]
78.81932
1.3941922

[110.18622, 110.701294, 110.35538, 108.861084, 108.77722, 112.72743, 115.345055, 113.20457, 108.739975, 109.816536, 111.1695]
110.89857
1.9961374

[157.42125, 157.53488, 154.36833, 156.93152, 160.18118, 465.06866, 154.26909, 158.74019, 155.63101, 161.65425]
188.18004
92.32328

[225.85762, 227.00928, 224.3857, 220.4849, 227.78426, 220.52733, 221.67104, 227.15007, 230.5581, 228.09575, 217.46976]
224.63579
3.8696914

[312.99905, 316.06506, 322.01227, 308.20938, 321.32565, 317.83002, 318.99982, 318.2494, 312.2661, 305.39874]
315.3355
5.230056

[441.30695, 457.5437, 431.40765, 448.03445, 455.044, 448.35077, 437.0946, 446.13696, 435.4886, 450.00037, 440.2012]
444.6008
7.848492

[630.6262, 625.9366, 640.4123, 642.63916, 630.5715, 1259.032, 637.36084, 635.3053, 629.1186, 639.4779]
697.04803
187.39935

[881.1056, 882.08264, 895.0495, 882.95496, 900.4094, 891.3415, 929.81476, 898.3446, 876.51764, 913.6774, 905.3233]
896.05646
15.242393

[1241.9989, 1238.2261, 1267.8279, 1266.3162, 1237.3475, 1240.6415, 1261.1848, 1230.0984, 1288.2704, 1228.265]
1250.0177
18.6884

[1796.2976, 1761.2257, 1826.4304, 1777.844, 1759.7052, 1779.8562, 1747.4512, 1733.3009, 1826.1221, 1739.2216, 1738.8176]
1771.4794
31.79214

[2564.4438, 2482.4966, 2564.3823, 2485.7188, 2532.796, 2563.6257, 2507.8784, 2530.5405, 2484.297, 2452.1765]
2516.8354
38.244366

[3493.07, 3470.2747, 3615.508, 3517.9001, 3603.2178, 3615.4707, 3607.443, 3659.7512, 3476.5906, 3594.5928, 3516.8328]
3560.9685
63.630047

[5030.9746, 5084.7188, 5010.738, 5068.165, 4971.7627, 4944.7554, 5116.0522, 5005.59, 4981.196, 4874.0317]
5008.7983
67.59781

[6968.933, 7353.4785, 7123.912, 7361.4077, 7313.028, 7182.712, 7070.0225, 7241.7256, 7205.077, 7111.6304, 7232.488]
7196.765
116.49191

[9844.326, 9895.712, 9787.648, 9900.296, 9961.161, 10041.238, 10124.823, 10155.189, 10020.463, 10286.446]
10001.7295
146.785

[14024.953, 13947.241, 14168.365, 13960.973, 13868.412, 14726.781, 14532.979, 13977.096, 14021.731, 13905.472, 14448.276]
14143.844
277.34982

[20643.045, 20632.568, 20604.756, 20388.932, 20072.137, 20075.8, 20238.777, 19621.744, 20663.535]
20326.809
336.76917