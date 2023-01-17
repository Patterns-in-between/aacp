#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
from statistics import median

import link

bpc = 4 # beats per cycle

samplerate = 25

# Initialise link with default tempo of 120
linkclock = link.Link(120)
linkclock.enabled = True
time.sleep(2)
s = linkclock.captureSessionState()
cps = (s.tempo() / bpc) / 60

print("current cps: %f" % cps)

def setTempo(bpm):
    state = linkclock.captureSessionState()
    state.setTempo(bpm, linkclock.clock().micros());
    linkclock.commitSessionState(state);

subname = b"adjusted"
addr = 'tcp://localhost:5555'

try:
    osc_server = liblo.Server(7070)
except liblo.ServerError as err:
    print(err)
    sys.exit()


def incoming(self, floats):
  total = 0.0
  maximum = 0.0
  signal_freqs = []
  cps_values = []
  
  for i in range(0,8):
    self._data.XData[i].append(self._data.XData[i][-1] + 1)
    self._data.YData[i].append((floats[i] * 2) - 1)

    if (len(self._data.YData[i]) > 250):
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
      
      lag = -1
      if len(peaks) > 0:
        # find first peak with a confidence of 0.6 or greater
        for peak in peaks:
          if self._data.conf[i][peak] >= 0.6:
            lag = peak
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
      cps_value = median(cps_values)
      print("multiple cps results: " + str(cps_values))
    else:
      cps_value = cps_values[0]
    print("set cps: %f" % cps_value)
    liblo.send(target, "/ctrl", "sensedcps", float(cps_value))
    setTempo(cps_value*60*2)
  
def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size // 2:]


if len(sys.argv) < 2:
    print("deva or juan?")
    exit(-1)

person = sys.argv[1]

try:
    target = liblo.Address("localhost", 6010)
except (liblo.AddressError, err):
    print(str(err))
    sys.exit()

class Data():

    def __init__(self):

        self.XData = [[0],[0],[0],[0],[0],[0],[0],[0]]
        self.YData = [[0],[0],[0],[0],[0],[0],[0],[0]]
        self.freqs = [[0],[0],[0],[0],[0],[0],[0],[0]]
        self.mags  = [[0],[0],[0],[0],[0],[0],[0],[0]]
        self.conf  = [[0],[0],[0],[0],[0],[0],[0],[0]]
        self.peakxy  = [(2,1),(2,1),(2,1),(2,1),(2,1),(2,1),(2,1),(2,1)]

class Plot():
    def __init__(self, data):

        self._data = data
        fig, axs = plt.subplots(3,8)
        fig.suptitle(person)
        self.fftline = []
        self.sigline = []
        self.confline = []
        self.annotation = []
        
        for i in range(0,8):
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
        for i in range(0,8):
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
        context = zmq.Context()
        subscriberSocket = context.socket(zmq.SUB)
        subscriberSocket.connect(addr)
        subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)
        
        while True:
            osc_server.recv(0)
            if subscriberSocket.poll(timeout=1):
                message = subscriberSocket.recv_multipart()
                msg = str(message[0]) #.decode("utf-8")
                msg = re.sub(r"^b'","",msg)
                msg = re.sub(r";.*$","",msg)
                #print(msg)
                if True: # re.search(person, msg):
                    #print(msg)
                    numbers = re.findall("\d+[0-9\-e\.]*", msg)
                    floats = list(map(float, numbers))
                    incoming(self, floats)
                
data = Data()
plotter = Plot(data)
fetcher = Fetch(data)

def glove_callback(path, args):
  value = (args[0] - 0.2) * 2.5
  floats = [0,0,0,0,0,0,0,0]
  for i, arg in enumerate(args):
    floats[i] = float(arg)
  incoming(fetcher, floats)
osc_server.add_method("/glove", "ffffff", glove_callback)

def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))
osc_server.add_method(None, None, fallback)


fetcher.start()
plt.show()
#fetcher.join()
