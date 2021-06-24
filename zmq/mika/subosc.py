#!/usr/bin/python3

import zmq, liblo, sys, re, datetime, os, time
from pathlib import Path

logdir = "logs"



Path(logdir).mkdir(parents=True, exist_ok=True)

logname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.txt")

print("Writing log to " + logname)
logfh = open(os.path.join(logdir, logname), "w")

logfh.write("Log start: " + str(time.time_ns() * 1e-9) + "\n")


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
        logfh.write(str(time.time_ns() * 1e-9) + " | " + message + "\n")
        # Make sure it gets written
        logfh.flush()
        numbers = re.findall("\d+\.\d+", str(message))
        for i, value in enumerate(numbers):
            liblo.send(target, "/ctrl", "sensor" + str(i), float(value))
        print(numbers)
