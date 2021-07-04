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

subname = b"adjusted"
addr = 'tcp://slab.org:5555'

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
        fig.suptitle('Vertically stacked subplots')
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
            self.sigline[i].axes.relim()
            self.sigline[i].axes.autoscale_view()
        
            self.fftline[i].set_data(self._data.freqs[i], self._data.mags[i])
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
            if subscriberSocket.poll(timeout=1000):
                message = subscriberSocket.recv_multipart()
                msg = str(message[0]) #.decode("utf-8")
                msg = re.sub(r"^b'","",msg)
                msg = re.sub(r";.*$","",msg)
                #print(msg)

                if re.search("deva", msg):
                    numbers = re.findall("\d+\.?\d*", msg)
                    floats = list(map(float, numbers))
                    
                    # print("oh: " + str(floats))
                    #print("updating data")
                    # add data to data class
                    total = 0.0
                    for i in range(0,8):
                        self._data.XData[i].append(self._data.XData[i][-1] + 1)
                        self._data.YData[i].append((floats[i] * 2) - 1)
                        
                        if (len(self._data.YData[i]) > 200):
                            self._data.YData[i].pop(0) # remove first frequency
                            self._data.XData[i].pop(0)
                            
                            x = self._data.YData[i]
                            t = self._data.XData[i]
                            
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
                            except:
                                print("oops")
                    print("avg: " + str(total/8))
                    liblo.send(target, "/ctrl", "cpssend", float(total/8))

                
data = Data()
plotter = Plot(data)
fetcher = Fetch(data)

fetcher.start()
plt.show()
#fetcher.join()
