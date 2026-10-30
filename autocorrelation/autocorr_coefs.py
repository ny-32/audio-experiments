import numpy as np

def autocorr(s, p, w=1):
    s = np.array(s, dtype=float)
    R = []
    s = s * w
    for i in range(p+1):
        R.append(np.dot(s[:s.size-i], s[i:]))
    return np.array(R)