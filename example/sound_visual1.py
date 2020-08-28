import pyaudio
import numpy as np
import pylab
import time

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second

def soundplot(stream):
    t1=time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    pylab.plot(data)
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2,2**16/2])
    pylab.savefig("03.png",dpi=200)
    pylab.close('all')
    print("took %.02f ms"%((time.time()-t1)*1000))
    
def listdevice():
    host_info = p.get_host_api_info_by_index(0)    
    device_count = host_info.get('deviceCount')
    devices = []

    # iterate between devices:
    for i in range(0, device_count):
        device = p.get_device_info_by_host_api_device_index(0, i)
        devices.append(device['name'])
    return devices


if __name__=="__main__":
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    #for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
    try:
        while True:    
            soundplot(stream)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()