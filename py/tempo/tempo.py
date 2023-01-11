#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import random
import time
import zmq
import re
import liblo
import sys

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
  for i in range(0,8):
    self._data.XData[i].append(self._data.XData[i][-1] + 1)
    self._data.YData[i].append((floats[i] * 2) - 1)
    
    if (len(self._data.YData[i]) > 150):
      self._data.YData[i].pop(0) # remove first frequency
      self._data.XData[i].pop(0)
                            
      x = self._data.YData[i]
      t = self._data.XData[i]

      a = autocorr(x)
                            
      ft = np.fft.rfft(x)
      freqs = np.fft.rfftfreq(len(x), 1/20) # Get frequency axis from the time axis
      mags = abs(ft) # We don't care about the phase information here
      self._data.freqs[i] = freqs[1:]
      self._data.mags[i] = mags[1:]
                            
      try: 
        inflection = np.diff(np.sign(np.diff(mags)))
        peaks = (inflection < 0).nonzero()[0] + 1
        peak = peaks[mags[peaks].argmax()]
        signal_freq = freqs[peak]
        #print(str(i) + ": " + str(signal_freq))
        total = total + signal_freq
        if signal_freq > maximum:
          maximum = signal_freq
        signal_freqs.append(signal_freq)
      except:
        print("oops")
      print("avg: %.2f max: %.2f" % (total/8, maximum))
      if len(signal_freqs) == 8:
        print("%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % tuple(signal_freqs))
        for x in range(0, 8):
          liblo.send(target, "/ctrl", "cps" + str(x), float(signal_freqs[x]))
      liblo.send(target, "/ctrl", "cpsavg", float(total/8))
      liblo.send(target, "/ctrl", "cpsmax", float(maximum))
    
  
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


class Plot():
    def __init__(self, data):

        self._data = data
        fig, axs = plt.subplots(2,8)
        fig.suptitle(person)
        self.fftline = []
        self.sigline = []
        
        for i in range(0,8):
            fftline, = axs[0,i].plot(0, 0)
            self.fftline.append(fftline)
            sigline, = axs[1,i].plot(0, 0)
            self.sigline.append(sigline)
            
        self.ani = FuncAnimation(plt.gcf(), self.run, interval = 200, repeat=True)

    def run(self, x):  
        #print("plotting data")
        for i in range(0,8):
            self.sigline[i].set_data(self._data.XData[i], self._data.YData[i])
            self.fftline[i].set_data(self._data.freqs[i], self._data.mags[i])
            
            self.sigline[i].axes.relim()
            self.sigline[i].axes.autoscale_view()
            self.fftline[i].axes.relim()
            self.fftline[i].axes.autoscale_view()

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
                print(msg)
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
