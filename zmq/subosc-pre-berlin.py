#!/usr/bin/env python3

import zmq, liblo, sys, re, datetime, os, time
from pathlib import Path

logdir = "logs"

subnames = [b"face", b"carpet", b"carpet_list_bang", b"hair_L", b"hair_S", b"knee_J", b"knee_D", b"hand", b"alexfader", b"alexbang"]

log = False

# body_parts = ["lfoot", "rfoot", "lbelly", "rbelly", "lshoulder", "rshoulder", "lback", "rback"]

if log:
    Path(logdir).mkdir(parents=True, exist_ok=True)
    logname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.txt")
    print("Writing log to " + logname)
    logfh = open(os.path.join(logdir, logname), "w")

    logfh.write("Log start: " + str(time.time()) + "\n")

try:
    target = liblo.Address("localhost", 6010)
    targetp5 = liblo.Address("localhost", 6011)
except (liblo.AddressError, err):
    print(str(err))
    sys.exit()

xpub_addr = 'tcp://192.168.0.10:5555'
context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect(xpub_addr)

for subname in subnames:
    subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)

while True:
    if subscriberSocket.poll(timeout=1000):
        message = subscriberSocket.recv_multipart()
        # print(message)
        msg = str(message[0]) #.decode("utf-8")
        msg = re.sub(r"^b'","",msg)
        msg = re.sub(r";.*$","",msg)


        # print(msg)
        if log:
            logmsg = str(time.time()) + " | " + msg + "\n"
            #print(logmsg)
            logfh.write(logmsg)
            # Make sure it gets written
            logfh.flush()

        m = re.search("carpet ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            on = m.group(1)
            number = m.group(2)
            
            liblo.send(target, "/ctrl", "carpet", float(number))
            continue

        m = re.search("hand ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            liblo.send(target, "/ctrl", "hand1", float(m[1]))
            liblo.send(target, "/ctrl", "hand2", float(m[2]))
            liblo.send(target, "/ctrl", "hand3", float(m[3]))
            liblo.send(target, "/ctrl", "hand4", float(m[4]))
            liblo.send(target, "/ctrl", "hand5", float(m[5]))
            continue
        
        m = re.search("carpet_list_bang ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            for i in range(0,13):
                #print("Sending %s = %f" % ("carpet%d" % (i), float(m.group(i+1))))
                liblo.send(target, "/ctrl", ("bang%d" % (i)), float(m.group(i+1)))
            continue

        m = re.search("carpet_list ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            for i in range(0,13):
                #print("Sending %s = %f" % ("carpet%d" % (i), float(m.group(i+1))))
                liblo.send(target, "/ctrl", ("carpet%d" % (i)), float(m.group(i+1)))
            continue
        
        
        m = re.search("hair_L ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
#            b = m.group(2)
            
            liblo.send(target, "/ctrl", "hairL", float(a))
            print("Sending hairL %f" % (float(a)))

        m = re.search("hair_S ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
#            b = m.group(2)
            
            liblo.send(target, "/ctrl", "hairS", float(a))
            print("Sending hairS %f" % (float(a)))
            
        m = re.search("knee_D ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
            b = m.group(2)
            
            liblo.send(target, "/ctrl", "kneeDa", float(a))
            liblo.send(target, "/ctrl", "kneeDb", float(b))
            print("Sending kneeD %f %f" % (float(a), float(b)))

        m = re.search("face ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
            b = m.group(2)
            
            liblo.send(target, "/ctrl", "facea", float(a))
            liblo.send(target, "/ctrl", "faceb", float(b))
            print("Sending face %f %f" % (float(a), float(b)))


        m = re.search("(alexfader|alexlist) ([0-9\.]+)", msg)
        if m:
            name = m.group(1)
            value = m.group(2)
            
            liblo.send(target, "/ctrl", name, float(value))
            print("Sending %s %f" % (name, float(value)))
            
