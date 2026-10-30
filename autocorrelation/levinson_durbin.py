import numpy as np

def coefs(r):
    r = np.array(r)
    p = r.size - 1
    a = np.array([1.0])
    epsilon = r[0]

    for j in range(1, p+1):
        gamma = (-1.0 * np.dot(r[1:j+1], a[::-1]) / epsilon)
        a = np.concat((a, [0])) + gamma * np.concat(([0], a[::-1]))
        epsilon = epsilon * (1 - np.pow(np.abs(gamma), 2))

    return a, epsilon