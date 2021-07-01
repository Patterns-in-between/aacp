#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import random
import time
import zmq
import re

subname = b"sensors"
addr = 'tcp://slab.org:5555'

class Data():

    def __init__(self):

        self.XData = [0]
        self.YData = [0]
        self.freqs = [0]
        self.mags = [0]
        self.acf = [0]
        self.inflection = [0]


class Plot():
    def __init__(self, data):

        self._data = data
        self.hLine, = plt.plot(0, 0)
        self.ani = FuncAnimation(plt.gcf(), self.run, interval = 50, repeat=True)

    def run(self, i):  
        #print("plotting data")
        #self.hLine.set_data(self._data.XData, self._data.YData)
        self.hLine.set_data(self._data.freqs, self._data.mags)
        self.hLine.axes.relim()
        self.hLine.axes.autoscale_view()

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
            if subscriberSocket.poll(timeout=1000):
                message = subscriberSocket.recv_multipart()
                msg = str(message[0]) #.decode("utf-8")
                msg = re.sub(r"^b'","",msg)
                msg = re.sub(r";.*$","",msg)
                numbers = re.findall("\d+\.?\d*", msg)
                floats = list(map(float, numbers))
                
                # print("oh: " + str(floats))
                #print("updating data")
                # add data to data class
                self._data.XData.append(self._data.XData[-1] + 1)
                self._data.YData.append((floats[1] * 2) - 1)

                if (len(self._data.YData) > 100):
                    if (len(self._data.YData) > 400):
                        self._data.YData.pop(0)
                        self._data.XData.pop(0)

                    x = self._data.YData
                    t = self._data.XData
                    
                    ft = np.fft.rfft(x)
                    freqs = np.fft.rfftfreq(len(x), t[1]-t[0]) # Get frequency axis from the time axis
                    mags = abs(ft) # We don't care about the phase information here
                    self._data.freqs = freqs[1:]
                    self._data.mags = mags[1:]

                    inflection = np.diff(np.sign(np.diff(mags)))
                    peaks = (inflection < 0).nonzero()[0] + 1
                    peak = peaks[mags[peaks].argmax()]
                    signal_freq = freqs[peak] # Gives 0.05
                    print(str(signal_freq))
                    
                    #acf = np.correlate(self._data.YData, self._data.YData, 'same')[-len(self._data.XData):]
                    #self._data.acf = acf
                    #print(str(acf.argsort()))
                    #inflection = np.diff(np.sign(np.diff(acf))) # Find the second-order differences
                    #self._data.inflection = inflection
                    #print(str(acf))
                    #print(str(inflection))
                    #peaks = (inflection < 0).nonzero()[0] + 1 # Find where they are negative
                    #delay = peaks[acf[peaks].argmax()] # Of those, find the index with the maximum value
                    #print("delay: " + str(delay))

print("oh")
data = Data()
plotter = Plot(data)
fetcher = Fetch(data)

fetcher.start()
plt.show()
#fetcher.join()
