import numpy as np
from vowel_synthesis import glottal_source, cascade
from formant_tracker import frame
from autocorrelation import autocorr_coefs as ac
from autocorrelation import levinson_durbin as ld
import scipy.signal as sig
import matplotlib.pyplot as plt
from autocorrelation import pole_to_formant as ptof

fs = 16000
fau = [[640, 420], [1230, 940], [2550, 2350]]
bwau = [[80, 80], [70, 70], [140, 80]]
fi = [310, 2020, 2960, 4000, 5200]
bwi = [45, 200, 400, 610, 850]

signal = glottal_source.simple_synth(f0=[160, 140], dur=0.5)

signal = cascade.cascade(fau, bwau, fs, signal)
signal = np.diff(signal, prepend=0)
signal = signal / np.max(np.abs(signal))

signal = frame.tilt(signal)
frames = frame.slice(signal)

track = []
for fr in frames:
    fr = fr * sig.windows.hann(fr.size, sym=False)
    a, e = ld.coefs(ac.autocorr(fr, 15))
    w,h = sig.freqz([1], a, fs=16000)

    f, bw = ptof.formants(np.roots(a))
    row = np.zeros(3)
    row[:min(3, f.size)] = f[:3]
    track.append(row)

time = (np.arange(frames.shape[0]) * (0.01 * fs) + (0.0125 * fs)) / fs


actual = np.linspace(i[0], i[1], time.size)
error = []
relative_error = []
for i in range(track.size):
    err = abs(actual[i] - track[i])
    error.append(err)
    relative_error.append(err / actual[i])