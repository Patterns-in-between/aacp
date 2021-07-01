#!/usr/bin/python3

import zmq, liblo, sys, re, datetime, os, time
from pathlib import Path

logdir = "logs"

subname = b"sensors"

log = False

if log:
    Path(logdir).mkdir(parents=True, exist_ok=True)
    logname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.txt")
    print("Writing log to " + logname)
    logfh = open(os.path.join(logdir, logname), "w")

    logfh.write("Log start: " + str(time.time_ns() * 1e-9) + "\n")

try:
    target = liblo.Address("localhost", 6010)
    targetp5 = liblo.Address("localhost", 6011)
except (liblo.AddressError, err):
    print(str(err))
    sys.exit()

xpub_addr = 'tcp://slab.org:5555'
context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect(xpub_addr)
subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)
while True:
    if subscriberSocket.poll(timeout=1000):
        message = subscriberSocket.recv_multipart()
        print(str(message[0]))
        msg = str(message[0]) #.decode("utf-8")
        msg = re.sub(r"^b'","",msg)
        msg = re.sub(r";.*$","",msg)
        if log:
            logmsg = str(time.time_ns() * 1e-9) + " | " + msg + "\n"
            print(logmsg)
            logfh.write(logmsg)
            # Make sure it gets written
            logfh.flush()
        
        numbers = re.findall("\d+\.?\d*", msg)
        for i, value in enumerate(numbers):
            liblo.send(target, "/ctrl", "sensor" + str(i), float(value))
        floats = map(float, numbers)
        liblo.send(targetp5, "/all", *floats)
        print(numbers)
