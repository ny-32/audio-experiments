import numpy as np
from vowel_synthesis import glottal_source, cascade
import scipy as sp
from maad import util as maad

# to do: make it read segments and vowel data from files instead of hardcoding
fs = 16000
fae = [620, 1660, 2430]
bwae = [70, 150, 320]
fi = [310, 2020, 2960]
bwi = [45, 200, 400]
fa = [660, 1200, 2550]
bwa = [100, 70, 200]
fo = [540, 1100, 2300]
bwo = [80, 70, 70]
segments = [[440 / 4, 0.5, fa, bwa], [493.88 / 4, 0.5, fi, bwi], [523.25 / 4, 0.5, fo, bwo], [493.88 / 4, 0.5, fae, bwae]]

output_segments = []
for s in range(len(segments) - 1):
    signal = glottal_source.simple_synth(f0=segments[s][0], dur = segments[s][1] + 0.025)
    signal = cascade.cascade(segments[s][2], segments[s][3], fs, signal)
    signal = np.diff(signal, prepend=0)
    signal = signal / np.max(np.abs(signal))

    # signal1 = glottal_source.simple_synth(f0=segments[s][0], dur = segments[s][1] - 0.01)
    # signal1 = cascade.cascade(segments[s][2], segments[s][3], fs, signal1)
    # signal1 = np.diff(signal1, prepend=0)
    # signal1 = signal1 / np.max(np.abs(signal1))
# 
    # signal2 = glottal_source.simple_synth(f0=[segments[s][0], segments[s+1][0]], dur=0.01)
    # signal2 = cascade.cascade(np.stack([segments[s][2], segments[s+1][2]], axis=1), np.stack([segments[s][3], segments[s+1][3]], axis=1), fs, signal2)
    # signal2 = np.diff(signal2, prepend=0)
    # signal2 = signal2 / np.max(np.abs(signal2))
    # 
    # signal = np.concat([signal1, signal2])
    
    output_segments.append(signal)

s = len(segments) - 1
signal = glottal_source.simple_synth(f0=segments[s][0], dur = segments[s][1])
signal = cascade.cascade(segments[s][2], segments[s][3], fs, signal)
signal = np.diff(signal, prepend=0)
signal = signal / np.max(np.abs(signal))
output_segments.append(signal)

output = output_segments[0]
for i in range(1, len(output_segments)):
    output = maad.crossfade(output, output_segments[i], fade_len=0.05, fs=fs)
sp.io.wavfile.write("testaudio.wav", fs, ((output) * 32767 * 0.8).astype(np.int16))