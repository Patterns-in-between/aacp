#!/usr/bin/python3

run_osc = 0
run_link = 0
run_plot = 0
run_zmq = 0


import statsmodels.api as sm
# import numpy as np
from scipy.signal import find_peaks
import threading
import time
if run_zmq:
    import zmq
    import re
if run_osc:
    import liblo
if run_link:
    import link
if run_plot:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

if run_zmq:
    import zmq
    subname = "imu"
    addr = 'tcp://192.168.0.100:5555'
    
    context = zmq.Context()
    
    subscriberSocket = context.socket(zmq.SUB)
    subscriberSocket.connect(addr)
    subscriberSocket.setsockopt_string(zmq.SUBSCRIBE, subname)
    
import sys
import statistics
import math

samplerate = 20
window = 3 # in seconds
bpm = 60
bpc = 4
count = 0
sensorcount = 3

cps_target = 0.5

if run_osc:
    try:
        osc_server = liblo.Server(7070)
    except liblo.ServerError as err:
        print(err)
        sys.exit()

if run_link:
    linkclock = link.Link(120)
    linkclock.enabled = True
    time.sleep(2)
    s = linkclock.captureSessionState()
    bpm = s.tempo()

def setTempo(target, maxchange):
    global bpm, state
    new_cps = target

    # maximum value to change cps by
    maxchange = maxchange / samplerate
    # print("maxchange: %.4f" % (maxchange), samplerate)
    
    cps = (bpm / 60) / bpc
    change = new_cps - cps
    # print("target: %.2f" % (new_cps))
    
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
    bpm = new_bpm

    if run_link:
        print("setting %.4f" % bpm)
        state = linkclock.captureSessionState()
        state.setTempo(bpm, linkclock.clock().micros());
        linkclock.commitSessionState(state);


times = [time.time()]

def incoming(self, floats):
  global count, samplerate, times, cps_target
  times.append(time.time())
  samplerate = 1/ ((times[-1] - times[0]) / len(times))

  count = count + 1
  total = 0.0
  maximum = 0.0
  signal_freqs = []
  cps_values = []
  
  for i in range(0,sensorcount):
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
      cps_target = statistics.median(cps_values)
      #print("multiple cps results: " + str(cps_values))
    else:
      cps_target = cps_values[0]
  setTempo(cps_target, 0.5)

class Data():

    def __init__(self):
        self.XData = []
        self.YData = []
        self.freqs = []
        self.mags  = []
        self.conf  = []
        self.peakxy  = []

        for i in range(0,sensorcount):
            self.XData.append([0])
            self.YData.append([0])
            self.freqs.append([0])
            self.mags.append([0])
            self.conf.append([0])
            self.peakxy.append((2,1))

class Plot():
    def __init__(self, data):
        self._data = data
        fig, axs = plt.subplots(3,sensorcount)
        fig.suptitle("imu")
        self.fftline = []
        self.sigline = []
        self.confline = []
        self.annotation = []
        
        for i in range(0,sensorcount):
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
        for i in range(0,sensorcount):
            self.sigline[i].set_data(self._data.XData[i], self._data.YData[i])
            self.fftline[i].set_data(self._data.freqs[i], self._data.mags[i])
            self.confline[i].set_data(self._data.freqs[i], self._data.conf[i])

            (x,y) = self._data.peakxy[i]
            # peak position
            self.annotation[i].xy = (x,y)
            self.annotation[i].set(text= ("cps %.2f" % (1/x)))
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
        global samplerate
        
        while True:
            if run_osc:
                osc_server.recv(1000)

            if len(times) > 100:
                times.pop(0)
            # Get data here
            #floats = [1,1,1]
            #incoming(self, floats)

            # about imu. now it is publishihg to the proxy server via zmq hosted on 192.168.0.100, you should subscribe to “imu”. Data is list of 8 numbers [AccX, AccY, AccZ,GyroX, iGyroY, GyroZ,imu.roll, imu.pitch]
            if run_zmq:
                if subscriberSocket.poll(timeout=1):
                    message = subscriberSocket.recv_multipart()
                    print(message)
                    msg = str(message[1]) #.decode("utf-8")
                    msg = re.sub(r"^b'","",msg)
                    msg = re.sub(r"^\w+\s+","",msg) # remove name from start
                    msg = re.sub(r";.*$","",msg)
                    numbers = re.findall("\d+[0-9\-e\.]*", msg)
                    floats = list(map(float, numbers))
                    print(floats)
                    incoming(self, floats)

            
data = Data()
if run_plot:
    print("run plot")
    plotter = Plot(data)
fetcher = Fetch(data)
fetcher.start()

if run_osc:
    def osc_callback(path, args):
        floats = [0,0,0]
        for i, arg in enumerate(args):
            floats[i] = float(arg)
        incoming(fetcher, floats)
    osc_server.add_method("/alex", "fff", osc_callback)

    def fallback(path, args, types, src):
        print("got unknown message '%s' from '%s'" % (path, src.url))
        for a, t in zip(args, types):
            print("argument of type '%s': %s" % (t, a))
    osc_server.add_method(None, None, fallback)

if run_plot:
    plt.show()
#fetcher.join()

# 192.168.0.100 / imu

