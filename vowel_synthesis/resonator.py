import numpy as np
import scipy as sp

def res_filter(f, bw, fs, x):
    t = 1 / fs
    upd_int = int(0.005 * fs)
    blocks = int(np.ceil(x.size / upd_int))

    f = np.atleast_1d(f)

    if (f.size == 1):
        f = np.repeat(f, 2)
    f = np.linspace(f[0], f[1], blocks)

    bw = np.atleast_1d(bw)

    if (bw.size == 1):
        bw = np.repeat(bw, 2)
    bw = np.linspace(bw[0], bw[1], blocks)

    filter_output = []
    pos = 0
    zf = [0, 0]
    for freq, band in zip(f, bw):
        c = -np.exp(-2 * np.pi * band * t)
        b = 2 * np.exp(-1.0 * np.pi * band * t) * np.cos(2 * np.pi * freq * t)
        a = 1 - b - c
        temp = x[pos:(pos+upd_int)]
        temp, zf = sp.signal.lfilter([a], [1, -1 * b, -1 * c], temp, zi=zf)
        filter_output.append(temp)
        pos += upd_int

    return np.concatenate(filter_output)