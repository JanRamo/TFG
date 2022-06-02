from genericpath import exists
import json, math
from os import path
import numpy as np
import essentia.standard as es
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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

filename = 'data_vco1_tri.json'
SignalData = []
objectNumber = 3 
# Check if file exists
if path.isfile(filename) is False:
    raise Exception("File not found")
    
# Read JSON file
with open(filename) as fp:
        SignalData = json.loads(fp.read())

pitchFrequency = np.round(SignalData[objectNumber]['Pitch Frequency'])
sineFrequencies = np.round(np.array(SignalData[objectNumber]['Sine Frequency']))
harmonicFrequencies = np.round(np.array(SignalData[objectNumber]['Harmonics']))
harmonicMagnitudes = np.round(np.array(SignalData[objectNumber]['Magnitud']))
harmonicPhases = np.array(SignalData[objectNumber]['Phase'])

maxHarm = len(sineFrequencies)

harm = np.empty(maxHarm)
for j in range (0,maxHarm):
    #p = harmArray.append(j)
    harm[j] = pitchFrequency*j

#print(harm)
print(harmonicFrequencies)
print(harmonicMagnitudes)

# realHarm = []
# for x in sineFrequencies:
#     #print(x)
#     exist = x in harm       
#     #print(exist)   
#     if exist == True:
#         realHarm.append(x)
#         #print(realHarm)
#     if exist == False:
#         print('cañita brava')

    
for x in harmonicFrequencies:
    harmonicNumber = np.round(harmonicFrequencies/pitchFrequency)

#Relation between magnitudes
relationArray= []
for magnitud in harmonicMagnitudes:
    relationNumber  = harmonicMagnitudes[0]/magnitud
    relationArray.append(relationNumber)

roundedRelationArray = np.round(relationArray,1)
print(roundedRelationArray)
print(harmonicNumber)

_, ax = plt.subplots(2,1, figsize=(10, 6))
# frequency_stamps = np.linspace(0, params["sampleRate"] / 2, int(params["frameSize"]/ 2) + 1)
#plt.plot(harmonicNumber)
# ax[0].set_ylim([-120, -20])
ax[0].bar(harmonicNumber, harmonicMagnitudes + 100, width=1, edgecolor="white", linewidth=0.7, bottom = -100)
ax[0].set_xlabel("Harmonic Number")
ax[0].set_xlim(left = 0.5)
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].set_ylabel("Magnitude [dBFS]")
# ax.set_ylim([-100, 0])
ax[0].set_title("Analyzed Spectrum")

ax[1].bar(harmonicNumber, relationArray, width=1, edgecolor="white", linewidth=0.7)
ax[1].set_xlabel("Harmonic Number")
ax[1].set_xlim(left = 0.5)
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
for i, v in enumerate(roundedRelationArray):
    plt.text(harmonicNumber[i] - 0.5, v , str(v))
ax[1].set_ylabel("Magnitude [dBFS]")
ax[1].set_ylim([0, 1])
ax[1].set_title("Analyzedss Spectrum")

plt.suptitle("Analized Signal")
plt.tight_layout()
plt.savefig("Harmonics.png")
plt.show()
plt.clf()
#convertedArray = harmonicFrequencies.astype(np.float) 
# print(type(harmonicFrequencies))
# print(harmonicFrequencies)
#print(np.float32(harmonicFrequencies))