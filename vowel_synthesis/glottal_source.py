# glottal sound source synth

import numpy as np
import scipy as sp
from vowel_synthesis import resonator
import matplotlib.pyplot as plt

# voicing source
#   specify: F0 (fundamental freq of voicing), AV (amplitude of normal voicing)

def simple_synth(fs=16000, f0=160, av=30.0, dur=1.0):
    sig_len = int(fs*dur)
    signal = np.zeros(sig_len)
    f0 = np.atleast_1d(f0)
    if f0.size == 1:
        f0 = np.repeat(f0, 2)
    f0 = np.linspace(f0[0], f0[1], sig_len)
    
    # impulse train corresponding to normal voicing is generated whenever F0>0
    #   amp of each impulse is determined by AV
    #   # of samples between impulses = sample rate / F0

    #period = fs/f0
    #pulse_pos = np.arange(0, sig_len, period).astype(int)
    #signal[pulse_pos] = av

    pos = 0
    phas = 0
    signal[pos] = av
    while pos < sig_len:
        phas += f0[pos] / fs
        if phas >= 1:
            phas -= 1
            signal[pos] = av
        pos += 1

    # impulse train --> through lowpass filter
    #   -> typical glottal volume velocity waveform
    #   glottal resonator frequency FGP = 0 Hz
    #   glottal resonator bandwidth BGP = 100 Hz
    # signal = signal * sp.signal.windows.hann(signal.size, sym=False)
    return resonator.res_filter(0, 100, fs, signal)
#
#def to_dB(H):
#    return 20 * np.log10(np.maximum(H, 1e-12))
#
#def norm(H):
#    return H / np.max(np.abs(H))
#
#fs =
#voicing_source = synth()
#bins = np.fft.rfftfreq(voicing_source.size, 1/16000)
#plt.figure()
#plt.plot(bins, to_dB(np.abs(norm(np.fft.rfft(voicing_source)))))
#plt.xlim(0, 2000)
#plt.title("Spectrum of source")
#plt.show()