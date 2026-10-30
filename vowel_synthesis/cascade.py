import numpy as np
import scipy as sp
from vowel_synthesis import resonator

def cascade(f, bw, fs, x):
    nfc = np.shape(np.array(f))[0]
    signal = np.array(x)
    for i in range(nfc):
        signal = resonator.res_filter(f[i], bw[i], fs, signal)
    return signal