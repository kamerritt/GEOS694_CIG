"""
This script reads in seismic data from 11 of the 13 eruptions of Shishaldin 
Volcano that took place between July and November 2023. Using the equation
and corresponding parameters for seismic energy from Johnson and Aster (2005), 
this program calculates the total seismic energy (in Joules) for each of the 
11 events. It is then designed to compare these energy values with calculated
SO2 masses (Lopez et al., In prep.) to determine whether a relationship exists.
"""

# Import packages

import numpy as np
import math
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams, colormaps, colors
#import colorcet as cc
from obspy.clients.fdsn import Client
from obspy import Stream, Trace, UTCDateTime, read
import scipy.integrate as integrate
from geopy.distance import geodesic as GD

SVDIR = '/Users/kamerritt/Desktop/Shishaldin/energy_calcs/'

TOP_DIR = '/Users/kamerritt/Documents/'
MSEED_DIR = '/Users/kamerritt/PycharmProjects/shishaldin_research/'

# STA/LTA parameters
STA_WINDOW = 5
LTA_WINDOW = 60
THRESH_ON = 10.0
THRESH_OFF = .5

# Metadata 
NET = 'AV'
LOC = ''
CHAN = 'BHZ'
SEIS_STA = 'SSLS'

LOAD_MSEED = True
FONT_S = 16
rcParams.update({'font.size': FONT_S})

client = Client('IRIS')

# Event labels, excluding Events 7 and 9 due to windy/noisy infrasound
dict_keys = ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5', 'Event 6', 
             'Event 8', 'Event 10', 'Event 11', 'Event 12', 'Event 13']
dict = dict.fromkeys(dict_keys)

# Event numbers
evt_num = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13]

# Start and end times for all events (excluding 7 and 9)
starttimes = ['2023-7-14T05:31:41', '2023-7-16T00:08:05','2023-7-18T09:17:02', 
              '2023-7-22T13:17:10', '2023-7-26T09:26:45', '2023-8-04T01:24:52', 
              '2023-8-25T13:00:49', '2023-9-15T23:04:00', '2023-9-24T20:38:31', 
              '2023-10-03T03:36:54','2023-11-03T02:57:09']

endtimes = ['2023-7-14T11:25:12', '2023-7-16T07:20:13', '2023-7-18T16:50:43',
            '2023-7-23T08:32:53', '2023-7-26T19:10:00', '2023-8-04T16:35:32',
            '2023-8-26T02:17:26', '2023-9-16T05:28:59', '2023-9-25T14:30:38',
            '2023-10-03T16:22:25', '2023-11-03T15:02:08']

# Select timescale: 'utc' or 'dr'
timescale = 'utc'

# Define time to read data in before RSAM peak
START_OFF = 10 * 3600 
TIME_END = 10 * 3600 

FILT = [1, 10]

# Seismic energy parameters from Johnson & Aster (2005):
f = 2  
rho_e = 2000
# Chosen following Gestrich et al. (2020):
c_e = 1400  
Q = 50  
VLATLON = (54.7554, -163.9711)

SAVE = False

# Filtering out regional earthquakes for Events 2 and 6
regional_eqs = {2: [(UTCDateTime('2023-07-16T06:48:55'), 
                     UTCDateTime('2023-07-16T06:50:38'))],

                6: [(UTCDateTime('2023-08-03T19:34:19'), 
                     UTCDateTime('2023-08-03T19:36:29'))]}

#%% Function(s)

"""
Metadata for AV.SSLS.BHZ

NET = 'AV'
LOC = ''
CHAN = 'BHZ,BDF'
SEIS_STA = 'SSLS'
"""


class SeismicEnergy():
    trace = []
    time = []
    data = []
    energy = []

    def __init__(self, network, location, channel, station, starttime, endtime,
                attenuation, stats, delta, energy):
        self.network = network
        self.location = location
        self.channel = channel
        self.station = station
        self.starttime = starttime
        self.endtime = endtime
        self.attenuation = attenuation
        self.stats = stats
        self.delta = delta
        self.energy = energy

    def create_traces(self, network, location, channel, station, starttime, endtime):
        st = client.get_waveforms(network=network, station=station, 
                                location=location, channel=channel, 
                                starttime=starttime, endtime=endtime, 
                                attach_response=True)
        
        inv = client.get_stations(network=network, station=station,
                                channel=channel, level="response")
        
        for tr in st:
            coords = inv.get_coordinates(tr.id)
            tr.stats.longitude = coords['longitude']
            tr.stats.latitude = coords['latitude']
            tr.stats.elevation = coords['elevation']

        tr_filt = tr.filter('bandpass', freqmin=FILT[0], freqmax=FILT[1], corners=2, 
                zerophase=True)
        tr_taper = tr_filt.taper(max_percentage=0.05, type='hann')
         
        self.trace = tr_taper
        self.time = tr_taper.times
        self.data = tr_taper.data
    
    def remove_regional_eqs(self, eq_start, eq_end):
        tr_data_time = self.time('utcdatetime')
        mask = np.logical_and(tr_data_time >= eq_start, tr_data_time 
                                  <= eq_end)
        self.data[mask] = np.nan

    def remove_nans(self):
        valid_mask = ~np.isnan(self.data)
        data = self.data[valid_mask]

        self.data = data
        attenuation = math.exp((-math.pi * f * r) / (c_e * Q))
        self.attenuation = attenuation

    """
    Seismic energy equation parameters from Johnson and Aster (2005):
    r: Source-receiver distance
    rho_earth: Volcano material density
    c_earth: Fixed p-wave velocity
    A: Attenuation factor
    S: Seismic site response
    U: Particle velocity
    """
    def calculate_seismic_energy(self, r, rho_earth, c_earth, A, S_sq, U_sq, dt):
        int = integrate.trapezoid(S_sq * U_sq, dx=dt)
        scalar = 2 * math.pi * (r ** 2) * rho_earth * c_earth * (1 / A)
        E_seismic = scalar * int

        return E_seismic


if __name__ == '__main__':
    
    for evt_tmp, starttime, endtime in zip(evt_num, starttimes, endtimes):
        SeismicEnergy.create_traces(self, NET, CHAN, SEIS_STA, starttime, endtime)
        if 
