import numpy as np
import time
import matplotlib.pyplot as plt
from obspy import read

# NumPy time = 1.017E-04s

def benchmark(func, *args, repeats=5):
    """Run a function several times and return the median runtime in seconds."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return np.median(times), result

def get_example_data(plot=False):
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

# Define input variablers used by the STA/LTA functions
x, sampling_rate = get_example_data()
nsta = int(sampling_rate * 0.5)
nlta = int(sampling_rate * 10)

def stalta_numpy(x, nsta, nlta):
    """Calculate STA/LTA with NumPy calls only"""
    n  = len(x)
    x2 = x ** 2                    # squared amplitude
    cs = np.cumsum(x2)             # cumulative sum of squared amplitude

    # Prepend a zero so that cs[i] - cs[i-w] gives the sum over w samples
    cs = np.concatenate([[0], cs])

    ratio = np.zeros(n)

    # Valid range: need at least nlta samples behind us
    i = np.arange(nlta, n)

    sta = (cs[i] - cs[i - nsta]) / nsta
    lta = (cs[i] - cs[i - nlta]) / nlta

    valid = lta > 0
    ratio[i[valid]] = sta[valid] / lta[valid]

    return ratio

time_numpy, result_numpy = benchmark(stalta_numpy, x, nsta, nlta)
print(f"NumPy:   {time_numpy:.3E} seconds")

plt.figure(figsize=(10, 4))
plt.plot(result_numpy)
plt.title('STA/LTA Ratio: NumPy')
plt.tight_layout()
plt.show()