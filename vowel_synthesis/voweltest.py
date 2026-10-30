import numpy as np
import scipy as sp
from vowel_synthesis import glottal_source
from vowel_synthesis import cascade

fs = 16000
signal = glottal_source.simple_synth(f0=[160, 140], dur=0.5)

fi = [310, 2020, 2960, 4000, 5200]
bwi = [45, 200, 400, 610, 850]
fae = [620, 1660, 2430]
bwae = [70, 150, 320]
fau = [[640, 420], [1230, 940], [2550, 2350]]
bwau = [[80, 80], [70, 70], [140, 80]]


signal = cascade.cascade(fae, bwae, fs, signal)
signal = np.diff(signal, prepend=0)
signal = signal / np.max(np.abs(signal))
signal.tofile("signal", sep=",")
sp.io.wavfile.write("testaudio.wav", fs, ((signal) * 32767 * 0.8).astype(np.int16))
