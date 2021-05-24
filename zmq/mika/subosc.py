#!/usr/bin/python3

import zmq, liblo, sys, re

try:
    target = liblo.Address("localhost", 6010)
except (liblo.AddressError, err):
    print(str(err))
    sys.exit()

xpub_addr = 'tcp://slab.org:5555'
context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect(xpub_addr)
subscriberSocket.setsockopt(zmq.SUBSCRIBE, b"sensors")
while True:
    if subscriberSocket.poll(timeout=1000):
        message = subscriberSocket.recv_multipart()
        numbers = re.findall("\d+\.\d+", str(message))
        for i, value in enumerate(numbers):
            liblo.send(target, "/ctrl", "sensor" + str(i), value)
        print(numbers)
