#!/usr/bin/python3

import zmq, sys, re, datetime, os, time
from pathlib import Path

if len(sys.argv) < 2:
    print("please pass a log file")
    exit(-1)

logdir = sys.argv[1]

print("opening " + logdir)
f = open(logdir, "r")
header = f.readline()
m = re.search("Log start: (.*)", header)
if not m:
    print("Bad header")
    exit(-2)

logstart = float(m.group(1))
print("Log start time: " + str(logstart))

start = time.time() * 1e-9

xsub_addr = 'tcp://slab.org:5556'
context = zmq.Context()
publisherSocket = context.socket(zmq.PUB)
publisherSocket.connect(xsub_addr)
publishName = b"sensors"; #.encode('utf-8')


while (True):
    line = f.readline()
    if (not line):
        print("End of log.")
        exit(0)
        
    m = re.search("^(\S+)\s+\| (.*)", line)
    if not m:
        print("Couldn't parse line: " + line)
    else:
        logwhen = float(m.group(1))
        message = m.group(2)
        
        now = time.time() * 1e-9
        when = start + (logwhen - logstart)
        delay = when - now
        
        if delay > 0:
            time.sleep(delay)
        print(message.encode('utf-8'))
        publisherSocket.send_multipart([message.encode('utf-8')])


