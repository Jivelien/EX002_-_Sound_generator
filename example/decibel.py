import sounddevice as sd
from numpy import linalg as LA
import numpy as np
from time import sleep

duration = 60  # seconds

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print (str(volume_norm)+" "*15)
    sleep(1)

with sd.Stream(callback=print_sound):
    sd.sleep(duration * 1000)
