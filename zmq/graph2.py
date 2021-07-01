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


class Plot():
    def __init__(self, data):

        self._data = data
        self.hLine, = plt.plot(0, 0)
        self.ani = FuncAnimation(plt.gcf(), self.run, interval = 50, repeat=True)

    def run(self, i):  
        #print("plotting data")
        self.hLine.set_data(self._data.XData, self._data.YData)
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
                
                print("oh: " + str(floats))
                #print("updating data")
                # add data to data class
                self._data.XData.append(self._data.XData[-1] + 1)
                self._data.YData.append(floats[0])

                while (len(self._data.YData) > 200):
                    self._data.YData.pop(0)
                    self._data.XData.pop(0)
                

print("oh")
data = Data()
plotter = Plot(data)
fetcher = Fetch(data)

fetcher.start()
plt.show()
#fetcher.join()
