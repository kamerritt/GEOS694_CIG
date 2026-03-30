#import necessary packages
import obspy
from obspy.core import UTCDateTime
from obspy import UTCDateTime, read_inventory
from obspy.core.stream import Stream
from obspy.core.trace import Trace
from obspy.clients.fdsn import Client
from scipy.signal import spectrogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from obspy import read, read_inventory
from obspy.signal import filter
import numpy as np

"""concert start times
taylor swift n1: UTCDateTime('2023-07-23T02:40:05')
taylor swift n2: UTCDateTime('2023-07-24T02:40:05')
ed sheeran: UTCDateTime('2023-08-27T03:01:28')
beyonce: UTCDateTime('2023-09-15T02:40:05')
coldplay: UTCDateTime('2023-09-21 03:23:23')
the weeknd: UTCDateTime('2022-08-26 03:54:49')
the rolling stones: UTCDateTime('2024-05-16 04:18:50') 
metallica n1: UTCDateTime('2024-08-31 03:36:55')
metallica n2: UTCDateTime('2024-09-02 03:40:12')
"""
#taylor swift
starttime = UTCDateTime('2023-07-23T02:40:05')
endtime = UTCDateTime('2023-07-23T10:40:05') #eight hours after start



client = Client('IRIS')

st = client.get_waveforms('UW', 'KDK', '*', 'HNZ', starttime=starttime, endtime=endtime)
inv = client.get_stations(network='UW', station='KDK', channel='HNZ', level='response', starttime=starttime, endtime=endtime)

fs = st[0].stats.sampling_rate
st.merge(method=1, fill_value='latest')
st.detrend(type='demean')

tr = st[0]
tr.remove_response(inventory=inv, output='VEL')

tr_filt = tr.copy()
tr_filt.detrend(type='linear')
tr_filt.taper(max_percentage=0.02)
tr_filt.filter('bandpass', freqmin=0.1, freqmax=10, corners=2, zerophase=True)

#tr_filt.plot()

tvec_spec = st[0].times(type='matplotlib')
nper = int(20*tr.stats.sampling_rate)
f, t, Pspec = spectrogram(tr.data, fs=tr.stats.sampling_rate, window='hann', scaling='density', nperseg=nper, noverlap=0.5*nper)

Pspec_dB = 10 * np.log10(abs(Pspec) / np.power(1, 2))

plt.figure()
plt.pcolormesh(t, f, Pspec_dB, shading='auto', cmap='magma')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Taylor Swift N1 Frequencies')
plt.colorbar(label='Power (dB)')
plt.show()