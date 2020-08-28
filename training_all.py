import pyaudio
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from time import sleep

p = pyaudio.PyAudio()

base=32.70032
note={'do':0,'sid':0,
      'dod':1,'reb':1,
      're':2,
      'red':3,'mib':3,
      'mi':4,'fab':4,
      'fa':5,'mid':5,
      'fad':6,'solb':6,
      'sol':7,
      'sold':8,'lab':8,
      'la':9,
      'lad':10,'sib':10,
      'si':11,'dob':11}

def getNoteFreq(noteName,noteOcta):
        return base*pow(2,(note[noteName]+12*noteOcta)/12)


RATE = 44100 # time resolution of the recording device (Hz)
CHUNK = 16384 # number of data points to read at a time

FORMAT=pyaudio.paFloat32

CHANNEL=1 # 1 is microphone ; 2 is computer sound


stream = p.open(rate=RATE,channels=CHANNEL,format=FORMAT, input=True)

RECORDPERIOD=1
INITIALISATION=1
print("Initialisation")
for i in range((INITIALISATION)*int(RATE/CHUNK)):
        _ = stream.read(CHUNK)
    

print("Recording")
data = np.frombuffer(stream.read(CHUNK),dtype=np.float32)
for i in range(((RECORDPERIOD)*int(RATE/CHUNK))-1):
        data = np.concatenate((data, np.frombuffer(stream.read(CHUNK),dtype=np.float32)), axis=0)
    
stream.stop_stream()
stream.close()

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
# Recording Visualisation
time=list(frange(0,RECORDPERIOD,(1/RATE)))
plt.plot(time[:data.size],data)
plt.show()

# Extract FFT
fft=np.fft.rfft(data)
freq = np.fft.fftfreq(fft.size, d=1/RATE*2)
fftabs=np.absolute(fft)

plt.plot(freq,fftabs)
plt.ylim((0,max(fftabs[50:])))
plt.xlim((0,5000))

print(str(freq[50:][fftabs[50:].argmax()])+' Hz')
# FFT visualization
resample=1
fftabsResample=fftabs[::resample]
freqResample=freq[::resample]

peaks, peakVal = find_peaks(fftabsResample, height=ampPeak,distance=100)

plt.plot(freqResample,fftabsResample)
plt.plot(freqResample[peaks],fftabsResample[peaks],"x",color='red')
plt.ylim((0,max(fftabsResample[50:])))
plt.xlim((0,5000))

plt.show()
print(str(freqResample[50:][fftabsResample[50:].argmax()])+' Hz')
'''
# Rolling Mean
testAnicet=pd.DataFrame(fftabsResample).rolling(30,center = True).max().rolling(30, center=True).mean()
plt.plot(freqResample,testAnicet)

peaks, _ = find_peaks(testAnicet.iloc[:,0], height=200, threshold=0, distance=10)
plt.plot(freqResample[peaks],fftabsResample[peaks],"x",color='red')
plt.ylim((0,max(fftabsResample[50:])))
plt.xlim((1000,1500))


print(str(freqResample[50:][fftabsResample[50:].argmax()])+' Hz')
'''