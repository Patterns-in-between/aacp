#!/usr/bin/python3

# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import statsmodels.api as sm
import numpy as np
from scipy.signal import find_peaks
import threading
import random
import time
import zmq
import re
import liblo
import sys
import statistics
import math

samplerate = 40
window = 3 # in seconds
bpm = 60
bpc = 2


count = 0

def setTempo(target, maxchange):
    new_cps = target
    #print("bpm: %.2f" % (new_cps*60*bpc))
    # maximum value to change cps by
    maxchange = maxchange / samplerate
    #print("maxchange: %.2f" % (maxchange))
    
    cps = (bpm / 60) / bpc
    change = new_cps - cps
    print("target: %.2f" % (new_cps))
    
    if abs(change) > maxchange:
        if change > 0:
            new_cps = cps + maxchange
        else:
            new_cps = cps - maxchange
    else:
        new_cps = cps + change

        #print("current: %.2f new: %.2f difference: %.2f maxchange: %.2f" % (cps, new_cps, change, maxchange))

    new_bpm = new_cps*60*bpc
    print("set cps: %.2f target: %.2f old bpm: %.2f new bpm: %.2f" % (new_cps, target, bpm, new_bpm))


def incoming(self, floats):
  global count
  count = count + 1
  total = 0.0
  maximum = 0.0
  signal_freqs = []
  cps_values = []
  
  for i in range(0,3):
    self._data.XData[i].append(self._data.XData[i][-1] + 1)
    self._data.YData[i].append((floats[i] * 2) - 1)

    if (len(self._data.YData[i]) > (window * samplerate)):
      self._data.YData[i].pop(0) # remove first frequency
      self._data.XData[i].pop(0)
      
      x = self._data.YData[i]
      t = self._data.XData[i]
      
      # https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.acf.html
      # "if alpha=.05, 95 % confidence intervals
      # are returned where the standard
      # deviation is computed according to
      # Bartlett”s formula."
      auto = sm.tsa.acf(x, nlags=2000, alpha=.05)
      
      self._data.mags[i] = auto[0]
      self._data.conf[i] = auto[1][:, 1]

      # find peaks in autocorrelation
      peaks = find_peaks(auto[0])[0]

      if len(peaks) > 0:
          # find variance
          variance = 0
          try:
              variance = statistics.variance(auto[0])
              # print("variance: %.2f" % variance)
          except:
              pass

          rnge = 0
          last_second = x[0-math.floor(samplerate):]
          rnge = max(last_second) - min(last_second)

          # Ignore if range is low - performer isn't moving much
          if rnge > 0.1:
              lag = -1
              # find first peak with a confidence of 0.8 or greater
              for peak in peaks:
                  if self._data.conf[i][peak] >= 0.8:
                      lag = peak
                      #print("sensor %d cps %.2f conf %.2f range %.2f" % (i, 1/(peak/samplerate), self._data.conf[i][peak], rnge))
                      break
              if lag > -1:
                  self._data.peakxy[i] = (lag/samplerate,self._data.mags[i][lag])
                  cps_values.append(1/(lag/samplerate))
      else:
        self._data.peakxy[i] = (0,0)
                            
      # Time axis
      self._data.freqs[i] = list(map(lambda x: x / samplerate, range(0,len(self._data.mags[i]))))

  if len(cps_values) > 0:
    if len(cps_values) > 1:
      cps_value = statistics.median(cps_values)
      #print("multiple cps results: " + str(cps_values))
    else:
      cps_value = cps_values[0]
      setTempo(cps_value, 0.02)

class Data():

    def __init__(self):

        self.XData = [[0],[0],[0]]
        self.YData = [[0],[0],[0]]
        self.freqs = [[0],[0],[0]]
        self.mags  = [[0],[0],[0]]
        self.conf  = [[0],[0],[0]]
        self.peakxy  = [(2,1),(2,1),(2,1)]

class Fetch(threading.Thread):

    def __init__(self, data):

        threading.Thread.__init__(self)
        self._data = data
        self._period = 0.25
        self._nextCall = time.time()

    def run(self):
        global samplerate
        context = zmq.Context()
        
        times = [time.time()]
        while True:
            if len(times) > 100:
                times.pop(0)

            # Get data here
            floats = [1,1,1]
            incoming(self, floats)

            times.append(time.time())
            samplerate = 1/ ((times[-1] - times[0]) / len(times))

data = Data()
fetcher = Fetch(data)
fetcher.start()
#fetcher.join()

print("aha")