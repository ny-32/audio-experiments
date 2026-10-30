import numpy as np

def formants(poles, fs=16000):
    poles = np.array(poles)
    poles = poles[np.imag(poles) > 0]
    freq = np.array(fs * np.angle(poles) / (2 * np.pi))
    bw = np.array(-1.0 * np.log(np.abs(poles)) * fs / np.pi)

    # keep_index = (freq > 50) & (bw < 500)
    keep_index = np.all([np.greater(freq, 50), np.less(bw, 500)], axis=0)
    freq = freq[keep_index]
    bw = bw[keep_index]
    order = np.argsort(freq)
    freq = freq[order]
    bw = bw[order]
    
    return freq, bw