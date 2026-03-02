import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import pdb

class StreamGauge():
    time = []
    data = []
    units  = 'ft'  

    def __init__(self, fid, station_id, station_name, starttime, units):
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime
        
    def read_guage_file(self, fid):
        """
        Read USGS Guage data and convert date and time to minutes since start

        parameters
        fid (str): path to data

        returns
        timestamp (list): time in minutes since the start of the month
        hgt (np.array): gauge height in ft
        """
        #fid = '/Users/kamerritt/Desktop/phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt'
        date, time, hgt = np.loadtxt(fid, skiprows=28, usecols=[2,3,5], 
                                        dtype=str).T

        hgt = hgt.astype(float)
        days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
        hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
        mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

        timestamps = []
        for d, h, m in zip(days, hours, mins):
            timestamp = (d * 24 * 60) + (h * 60) + m
            timestamps.append(timestamp)
        
        self.time = timestamps
        self.data = hgt

        max_hgt = self.data.max()
        print(max_hgt)

        #return self.time, self.data

    def plot(self):
        #time, data = self.read_guage_file(self, fid)
        #time, data = StreamGauge.read_guage_file(self, fid)
    
        fig, ax = plt.subplots()
        ax.plot(self.time, self.data)
        ax.set_xlabel(f'Minutes since {self.starttime}')
        ax.set_ylabel(f'Water height ({self.units})')
        ax.set_title(f'Stream Gauge {self.station_id} at {self.station_name} starting at {self.starttime}')

        plt.show()

    def convert(self):
        hgt_m = []
        for hgt in self.data:
            m = hgt * 0.3048 #conversion from feet to meters
            hgt_m.append(m)

        self.data = hgt_m
        self.units = 'm'
        #breakpoint()

    def demean(self):
        mean = stats.mean(self.data)
        hgt_demeaned = []
        for hgt in self.data:
            demeaned = hgt - mean #subtracts the mean value of the data array from the data array
            hgt_demeaned.append(demeaned)

        self.data = hgt_demeaned

    def shift_time(self, offset):
        offset_t = []
        for t in self.time:
            offset = t + offset #offsets time axis by a user input amount of minutes
            offset_t.append(offset)
        
        self.time = offset_t

    def main(self):
      self.read_guage_file(fid)
      self.plot()

      self.convert()
      self.demean()
      self.shift_time(-100)
      self.plot()
    
class NOAAStreamGauge(StreamGauge):
        units = 'm'

        def convert(self):
            pass

        def read_guage_file(self, fid):
            super().read_guage_file(fid)
            print('I am a NOAA stream gauge')

if __name__ == "__main__":
    fids = ['/Users/kamerritt/Desktop/phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt', 
            '/Users/kamerritt/Desktop/phelan_creek_stream_guage_2024-10-07_to_2024-10-14.txt']
    
    starttimes = ['2024-09-07 00:00', '2024-10-07 00:00']
    
    for fid, starttime in zip(fids, starttimes):
        sg = StreamGauge(fid=fid, station_id="15478040", 
                        station_name="PHELAN CREEK", starttime=starttime, units='ft')
        
        sg.main()

    for fid, starttime in zip(fids, starttimes):
        sg = NOAAStreamGauge(fid=fid, station_id="15478040", 
                        station_name="PHELAN CREEK", starttime=starttime, units='ft')
        
        sg.main()