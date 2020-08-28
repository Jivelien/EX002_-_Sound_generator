import pyaudio
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import seaborn as sb

p = pyaudio.PyAudio()

RATE = 44100 # time resolution of the recording device (Hz)
PPS = 1/RATE
CHUNK = 16384 # number of data points to read at a time

FORMAT=pyaudio.paFloat32

CHANNEL=1 # 1 is microphone ; 2 is computer sound


stream = p.open(rate=RATE,channels=CHANNEL,format=FORMAT, input=True)

INITIALISATION=2
print("Initialisation")
for i in range((INITIALISATION)*int(RATE/CHUNK)):
        _ = stream.read(CHUNK)
    
print("Recording")



# Recording infinite loop
data = pd.DataFrame()
try:
    while stream.is_active():
        dataSample = np.frombuffer(stream.read(CHUNK),dtype=np.float32)
        dataSample = pd.DataFrame(dataSample)
        data= pd.concat([data,dataSample], ignore_index=True)
except:
    pass
finally:
    print('End of recording')
    stream.stop_stream()
    stream.close()
    

data=data.rename(columns={0:'record'})
data['time']=np.arange(0,len(data)*PPS, PPS)

plt.plot(data['time'],data['record'])
plt.show()
# Data to FFT
dataForFFT=pd.DataFrame()
timeStep=int(RATE/10)
i=0
while 10*CHUNK+i*timeStep < len(data):
    dataForFFT=dataForFFT.append(data[0+i*timeStep:CHUNK+i*timeStep].reset_index()['record'].T, ignore_index=True)
    i+=1

fft=np.fft.rfft(dataForFFT)
fft=abs(fft)
freq = np.fft.fftfreq(len(fft.T), d=1/RATE*2)
fftT=pd.DataFrame(fft.T)
fftT.columns=[round(timeStep*i/RATE,2) for i in range(len(fftT.T))]
fftT['freq']=[round(f,1) for f in freq]
fftT=fftT.set_index('freq')
fftGraph = fftT[fftT.index >= 0]
#fftGraph=fftGraph[fftGraph.index <= 1000]
sb.heatmap(fftGraph, cmap='viridis', vmax=20)
plt.plot(fftGraph[15])
