import numpy as np
import scipy as sp
def slice(signal, fs=16000):
    interval = int(0.01 * fs)
    dur = int(0.025 * fs)
    indices = (np.arange(0, signal.size - dur, interval)).astype(int)
    frames = np.array([signal[i:i+dur] for i in indices])
    return frames

def tilt(signal):
    return sp.signal.lfilter([1, -0.68], [1], signal)