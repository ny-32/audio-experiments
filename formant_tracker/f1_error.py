import numpy as np
from vowel_synthesis import glottal_source, cascade
from formant_tracker import frame
from autocorrelation import autocorr_coefs as ac
from autocorrelation import levinson_durbin as ld
import scipy.signal as sig
import matplotlib.pyplot as plt
from autocorrelation import pole_to_formant as ptof

def error(f0):
    fs = 16000
    fi = [310, 2020, 2960, 4000, 5200]
    bwi = [45, 200, 400, 610, 850]
    ftest = fi
    bwtest = bwi
    ftest = np.array([np.full(2, i) for i in ftest])
    bwtest = np.array([np.full(2, i) for i in bwtest])

    signal = glottal_source.simple_synth(f0=f0, dur=0.5)

    signal = cascade.cascade(ftest, bwtest, fs, signal)
    signal = np.diff(signal, prepend=0)
    signal = signal / np.max(np.abs(signal))

    signal = frame.tilt(signal)
    frames = frame.slice(signal)

    track = []
    for fr in frames:
        fr = fr * sig.windows.hann(fr.size, sym=False)
        a, e = ld.coefs(ac.autocorr(fr, 12))

        f, bw = ptof.formants(np.roots(a))
        row = np.full(3, np.nan)
        row[:min(3, f.size)] = f[:3]
        track.append(row)
    track = np.array(track)
    actual = []
    for i in ftest:
        actual.append(np.linspace(i[0], i[1], track.shape[0]))
    error = []
    relative_error = []
    for index in range(3):
        temp_error = []
        temp_relative_error = []
        for i in range(track.shape[0]):
            err = abs(actual[index][i] - track[i][index])
            temp_error.append(err)
            temp_relative_error.append(err / actual[index][i])
        error.append(temp_error)
        relative_error.append(temp_relative_error)

    return error, relative_error

def sweep():
    freqs = np.arange(100, 600, 3)
    results = [error(i) for i in freqs]
    median_errs = [[(np.nanmedian(i[0][j])) for i in results] for j in range(3)]
    rel_errs = [[(np.nanmedian(i[1][j])) for i in results] for j in range(3)]
    plt.figure()
    for i in median_errs:
        plt.plot(freqs, i)
    plt.figure()
    for i in rel_errs:
        plt.plot(freqs, i)
    plt.show()

sweep()