import numpy as np
cimport numpy as np

def stalta_cython(np.ndarray[double, ndim=1] x, int nsta, int nlta):
    cdef int n = len(x)
    cdef int i, j
    cdef double sta, lta
    cdef np.ndarray[double, ndim=1] ratio = np.zeros(n)
    cdef np.ndarray[double, ndim=1] x2    = x ** 2

    # Initialize at position nlta
    cdef double sta_sum = 0.0
    cdef double lta_sum = 0.0

    for j in range(nlta - nsta, nlta):
        sta_sum += x2[j]
    for j in range(0, nlta):
        lta_sum += x2[j]

    for i in range(nlta, n):
        sta_sum += x2[i]     - x2[i - nsta]
        lta_sum += x2[i]     - x2[i - nlta]

        if lta_sum > 0:
            ratio[i] = (sta_sum / nsta) / (lta_sum / nlta)

    return ratio