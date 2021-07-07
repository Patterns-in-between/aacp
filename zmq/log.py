#!/usr/bin/env python3

import zmq, sys, re, datetime, os, time
from pathlib import Path

logdir = "logs"
xpub_addr = 'tcp://slab.org:5555'
subnames = [b"adjusted", b"sensors", b"trained", b"sync"]

log = True

stripPack = True

if log:
    Path(logdir).mkdir(parents=True, exist_ok=True)
    logname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.txt")
    print("Writing log to " + logname)
    logfh = open(os.path.join(logdir, logname), "w")

    logfh.write("Log start: " + str(time.time()) + "\n")

context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect(xpub_addr)

for subname in subnames:
    subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)

while True:
    if subscriberSocket.poll(timeout=1000):
        message = subscriberSocket.recv_multipart()
        msg = str(message[0]) #.decode("utf-8")

        if stripPack:
            # remove puredata 'pack' stuff - couldn't find a spec for this..
            # maybe we should just keep it in the log?
            msg = re.sub(r"^b'","",msg)
            msg = re.sub(r";.*$","",msg)
        
        logmsg = str(time.time()) + " | " + msg + "\n"
        logfh.write(logmsg)
        # Make sure it gets written straight away
        logfh.flush()
