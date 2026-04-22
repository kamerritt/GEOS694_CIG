import numpy as np
import time
import matplotlib.pyplot as plt
from obspy import read
from stalta_cy import stalta_cython

# Cython time =

time_python = 1.480
time_numpy = 1.017E-04
time_numba = 0.008

def benchmark(func, *args, repeats=5):
    """Run a function several times and return the median runtime in seconds."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return np.median(times), result

def get_example_data(plot=True):
    """Returns 1Hz highpassed vertical (Z) component seismometer data"""
    st = read()
    st.filter("highpass", freq=1)
    st = st.select(component="Z")
    st.resample(100) 
    st.taper(0.05) # taper ends to 0

    # Pad zeros on front and back to allow STA/LTA to start running average
    n = len(st[0].data)
    data_out = np.hstack([np.zeros(n), st[0].data, np.zeros(n)])  # pad zeros

    if plot:
        st.plot()
    
    print(st[0].stats.sampling_rate)

    return data_out, st[0].stats.sampling_rate

x, sampling_rate = get_example_data()
nsta = int(sampling_rate * 0.5)
nlta = int(sampling_rate * 10)

def stalta_python(x, nsta, nlta):
    n = len(x)
    ratio = [0] * nlta  # pad zeros before we start STA/LTA

    for i in range(nlta, n):
        # STA: mean squared amplitude over short window
        sta = 0.0
        for j in range(i - nsta, i):
            sta += x[j] * x[j]
        sta /= nsta

        # LTA: mean squared amplitude over long window
        lta = 0.0
        for j in range(i - nlta, i):
            lta += x[j] * x[j]
        lta /= nlta

        if lta > 0:
            ratio.append(sta / lta)
        else:
            ratio.append(0)

    return np.array(ratio)

time_python, result_python = benchmark(
    stalta_python, x, nsta, nlta
)

# Define input variablers used by the STA/LTA functions
x, sampling_rate = get_example_data()
nsta = int(sampling_rate * 0.5)
nlta = int(sampling_rate * 10)

time_cython, result_cython = benchmark(stalta_cython, x,  nsta, nlta)

print(f"Cython: {time_cython:.3f} seconds")
print(f"Speedup vs Python:           {time_python     / time_cython:.1f}x")
print(f"Speedup vs NumPy:            {time_numpy      / time_cython:.1f}x")
print(f"Speedup vs Numba:      {time_numba      / time_cython:.1f}x")

np.testing.assert_allclose(result_python, result_cython, rtol=1e-5)
print("Results match.")