#Import packages
import obspy
from obspy import read
from obspy.clients.fdsn import Client
import pandas as pd
import numpy as np
import glob
import os
import re
from compute_metrics import compute_metrics
import traceback
from datetime import datetime, timedelta

#Define variables
FILT = [1, 10]
FILT_INF = [0.5, 10]
DR_WIN_LEN = 300
VLATLON = (54.7554, -163.9711)
station_label = 'SSLS_BDF'
output_csv = 'RMSP_SSLS_2023_updated.csv'
MSEED_DIR = '/Users/kamerritt/PycharmProjects/shishaldin_research/'

client = Client('IRIS')
inv = client.get_stations(network='AV', station='SSLS,SSLN,SSBA',
                              channel='BDF,BHZ', level="response")

def extract_evt_num(filename):
    match = re.search(r'event(\d+)', os.path.basename(filename))
    if match:
        return int(match.group(1))
    else:
        return float('inf')

mseed_files = sorted(glob.glob(f'{MSEED_DIR}event*_ssls_timeframe.mseed'), 
                     key=extract_evt_num)



records = []

#Read in miniseed files and extract lat/lon and elevation info
for mseed in mseed_files:
        st_raw = read(mseed)

        for tr in st_raw:
            coords = inv.get_coordinates(tr.id)
            tr.stats.longitude = coords['longitude']
            tr.stats.latitude = coords['latitude']
            tr.stats.elevation = coords['elevation']
            # st_raw = Stream(st_raw_bak[i])
        station = st_raw[0].stats.station
        filename = os.path.basename(mseed)
        evt_id = filename.split('_')[0]

        try:
            st_inf = obspy.Stream([st_raw.select(channel='BDF')[0]])
            tmpl_i, RMS_p, pe, fc, fd, fsd = compute_metrics(
                st_inf, process_taper=True, metric_taper=None, 
                filter_band=FILT_INF, window_length=DR_WIN_LEN, overlap=0.8,
                vlatlon=VLATLON)

            tmpl_i_1D = np.ravel(tmpl_i)
            RMS_p_1D = np.ravel(RMS_p)

            start_day = tmpl_i_1D[0]

            timestamps = [st_inf[0].stats.starttime.datetime 
                          + timedelta(days=(t-start_day)) for t in tmpl_i_1D]

            for ts, rms in zip(timestamps, RMS_p_1D):
                records.append({
                    'DateTime': ts,
                    'Station': station_label,
                    'RMSP_Pa': rms
                })

        except Exception as e:
            print('error -- skipping mseed')
            traceback.print_exc()

#Create a dataframe of records 
df = pd.DataFrame(records)
df['DateTime'] = pd.to_datetime(
    df['DateTime']).dt.strftime('%-m/%-d/%Y %I:%M:%S %p')

df.to_csv(output_csv, index=True)

#Compile RMS Pressure timeseries for all events
evt_times = [
    {"event": 1, "start": '2023-7-14T05:31:41', 
     "end": '2023-7-14T11:25:12'},
    {"event": 2, "start": '2023-7-16T00:08:05', 
     "end": '2023-7-16T07:20:13'},
    {"event": 3, "start": '2023-7-18T09:17:02', 
     "end": '2023-7-18T16:50:43'},
    {"event": 4, "start": '2023-7-22T13:17:10', 
     "end": '2023-7-23T08:32:53'},
    {"event": 5, "start": '2023-7-26T09:26:45', 
     "end": '2023-7-26T19:10:00'},
    {"event": 6, "start": '2023-8-04T01:24:52', 
     "end": '2023-8-04T16:35:32'},
    {"event": 8, "start": '2023-8-25T13:00:49', 
     "end": '2023-8-26T02:17:26'},
    {"event": 10, "start": '2023-9-15T23:04:00', 
     "end": '2023-9-16T05:28:59'},
    {"event": 11, "start": '2023-9-24T20:38:31', 
     "end": '2023-9-25T14:30:38'},
    {"event": 12, "start": '2023-10-03T03:36:54', 
     "end": '2023-10-03T16:22:25'},
    {"event": 13, "start": '2023-11-03T02:57:09', 
     "end": '2023-11-03T15:02:08'},
]

#Assemble data in an Excel-readable format
df = pd.read_csv(output_csv, parse_dates=["DateTime"])

results = []

for evt in evt_times:
    evt_id = evt['event']
    t_s = evt['start']
    t_e = evt['end']

    sub = df[(df["DateTime"] >= t_s) & (df["DateTime"] <= t_e)]

    if sub.empty:
        continue

    peak_row = sub.loc[sub['RMSP_Pa'].idxmax()]

    results.append({
        'Event': evt_id,
        'Peak_RMSP': peak_row['RMSP_Pa'],
        'Peak_Time': peak_row['DateTime'],
    })

    df_peaks = pd.DataFrame(results)
    df_peaks.to_csv('peak_rmsp_ssls_csv', index=False)

    print(df_peaks)