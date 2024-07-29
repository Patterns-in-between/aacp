#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statsmodels.api as sm
import numpy as np
from scipy.signal import find_peaks
import threading
import random
import time
#import zmq
import re
import liblo
import sys
import statistics
import math
import link

samplerate = 20

window = 3 # in seconds

bpc = 2 # beats per cycle

# Initialise link with default tempo of 120
linkclock = link.Link(120)
linkclock.enabled = True
time.sleep(2)
s = linkclock.captureSessionState()
cps = (s.tempo() / bpc) / 60

print("current cps: %f" % cps)

def setTempo(target, maxchange):
    new_cps = target
    #print("bpm: %.2f" % (new_cps*60*bpc))
    # maximum value to change cps by
    maxchange = maxchange / samplerate
    #print("maxchange: %.2f" % (maxchange))
    
    state = linkclock.captureSessionState()
    bpm = state.tempo()
    cps = (bpm / 60) / bpc
    

    change = new_cps - cps
    #print("target: %.2f" % (new_cps))
    
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
    state.setTempo(new_bpm, linkclock.clock().micros());
    linkclock.commitSessionState(state);

try:
    osc_server = liblo.Server(7070)
except liblo.ServerError as err:
    print(err)
    sys.exit()


count = 0
cps_temp = 0.0
def incoming(self, floats):
  global count
  count = count + 1
  #if count % 4 > 0:
  #return
  total = 0.0
  maximum = 0.0
  signal_freqs = []
  cps_values = []
  global cps_temp

  
  
  
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
          #last_second = x[0-math.floor(samplerate):]
          last_second = x[-25:]
          rnge = max(last_second) - min(last_second)
          #print("rnge: %.2f"% rnge)
          
          # Ignore if range is low - performer isn't moving much
          if rnge > 0.1:
              lag = -1
              # find first peak with a confidence of 1.2 or greater >> made it 0.5
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
      #setTempo(cps_temp, 0.2)

  if len(cps_values) > 0:
    if len(cps_values) > 1:
      cps_value = statistics.median(cps_values)
      #print("multiple cps results: " + str(cps_values))
    else:
      cps_value = cps_values[0]
    #print("set cps: %f" % cps_value)
    #liblo.send(target, "/ctrl", "sensedcps", float(cps_value))
    cps_temp = cps_value
    setTempo(cps_value, 0.4)
  else:
    cps_temp = 0.1

 
#if len(sys.argv) < 2:
#    print("deva or juan?")
#    exit(-1)

try:
    target = liblo.Address("localhost", 6010)
except (liblo.AddressError, err):
    print(str(err))
    sys.exit()

class Data():

    def __init__(self):

        self.XData = [[0],[0],[0]]
        self.YData = [[0],[0],[0]]
        self.freqs = [[0],[0],[0]]
        self.mags  = [[0],[0],[0]]
        self.conf  = [[0],[0],[0]]
        self.peakxy  = [(2,1),(2,1),(2,1)]

class Plot():
    def __init__(self, data):
        print("hmmm")
        self._data = data
        fig, axs = plt.subplots(3,3)
        fig.suptitle("xyz")
        self.fftline = []
        self.sigline = []
        self.confline = []
        self.annotation = []
        
        for i in range(0,3):
            confline, = axs[0,i].plot(0, 0)
            self.confline.append(confline)
            
            fftline, = axs[1,i].plot(0, 0)
            self.fftline.append(fftline)

            annotation = axs[1,i].annotate(
                'local max', xy=(2, 1), xytext=(3, 1.5),
                arrowprops=dict(facecolor='black', shrink=0.05),
            )
            self.annotation.append(annotation)
            
            sigline, = axs[2,i].plot(0, 0)
            self.sigline.append(sigline)
            
        self.ani = FuncAnimation(plt.gcf(), # get current figure
                                 self.run,
                                 interval = 200,
                                 repeat=True
                                 )

    def run(self, x):  
        #print("plotting data")
        for i in range(0,3):
            self.sigline[i].set_data(self._data.XData[i], self._data.YData[i])
            self.fftline[i].set_data(self._data.freqs[i], self._data.mags[i])
            self.confline[i].set_data(self._data.freqs[i], self._data.conf[i])

            (x,y) = self._data.peakxy[i]
            # peak position
            self.annotation[i].xy = (x,y)
            self.annotation[i].set(text= ("cps %.2f" % x))
            # annotation position
            self.annotation[i].set_position((x+0.1,y+0.1))
            
            self.sigline[i].axes.relim()
            self.sigline[i].axes.autoscale_view()
            self.fftline[i].axes.relim()
            self.fftline[i].axes.autoscale_view()
            self.confline[i].axes.relim()
            self.confline[i].axes.autoscale_view()

class Fetch(threading.Thread):

    def __init__(self, data):

        threading.Thread.__init__(self)

        self._data = data
        self._period = 0.25
        self._nextCall = time.time()

    def run(self):
        times = [time.time()]
        while True:
            osc_server.recv(0)

data = Data()
#plotter = Plot(data)
fetcher = Fetch(data)

def xyz_callback(path, args):
  print("xyz")
  value = (args[0] - 0.2) * 2.5
  floats = [0,0,0]
  for i, arg in enumerate(args):
    floats[i] = float(arg)
  incoming(fetcher, floats)
osc_server.add_method("/xyz", "fff", xyz_callback)

def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))
osc_server.add_method(None, None, fallback)

print("hmm")
fetcher.start()
print("hmm")

plt.show()
#fetcher.join()
