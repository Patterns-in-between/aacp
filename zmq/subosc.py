#!/usr/bin/env python3

# amount
# position
# acceleration
# threshold

import zmq, liblo, sys, re, datetime, os, time
from pathlib import Path

logdir = "logs"

# subnames = [b"carpet", b"carpet_list_bang", b"hair_L", b"hair_S", b"knee_J", b"knee_D"]
subnames = [b"textile1", b"textile2", b"textile3", b"deva", b"juan", b"lizzie", b"alex"]

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

        m = re.search("textile1 ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            e = m.group(5)
            
            liblo.send(target, "/ctrl", "textile1a", float(a))
            liblo.send(target, "/ctrl", "textile1b", float(b))
            liblo.send(target, "/ctrl", "textile1c", float(c))
            liblo.send(target, "/ctrl", "textile1d", float(d))
            liblo.send(target, "/ctrl", "textile1e", float(e))
            # print("Sending textile1 %f %f %f %f" % (float(a), float(b), float(c), float(d)))
            continue

        m = re.search("textile2 ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            e = m.group(5)
            
            liblo.send(target, "/ctrl", "textile2a", float(a))
            liblo.send(target, "/ctrl", "textile2b", float(b))
            liblo.send(target, "/ctrl", "textile2c", float(c))
            liblo.send(target, "/ctrl", "textile2d", float(d))
            liblo.send(target, "/ctrl", "textile2e", float(e))
            # print("Sending textile2 %f %f %f %f" % (float(a), float(b), float(c), float(d)))
            continue


        m = re.search("textile3 ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            e = m.group(5)
            
            liblo.send(target, "/ctrl", "textile3a", float(a))
            liblo.send(target, "/ctrl", "textile3b", float(b))
            liblo.send(target, "/ctrl", "textile3c", float(c))
            liblo.send(target, "/ctrl", "textile3d", float(d))
            liblo.send(target, "/ctrl", "textile3e", float(e))
            # print("Sending textile3 %f %f %f" % (float(a), float(b), float(c)))
            continue

        m = re.search("deva ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg) 
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            
            liblo.send(target, "/ctrl", "deva1a", int(a))
            liblo.send(target, "/ctrl", "deva1b", float(b))
            liblo.send(target, "/ctrl", "deva2a", int(c))
            liblo.send(target, "/ctrl", "deva2b", float(d))
            print("Sending deva %i %f %i %f" % (int(a), float(b), int(c), float(d)))
            continue

        m = re.search("juan ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg) 
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            
            liblo.send(target, "/ctrl", "juan1a", int(a))
            liblo.send(target, "/ctrl", "juan1b", float(b))
            liblo.send(target, "/ctrl", "juan2a", int(c))
            liblo.send(target, "/ctrl", "juan2b", float(d))
            print("Sending juan %i %f %i %f" % (int(a), float(b), int(c), float(d)))
            continue

        m = re.search("lizzie ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg) 
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            
            liblo.send(target, "/ctrl", "lizzie1a", int(a))
            liblo.send(target, "/ctrl", "lizzie1b", float(b))
            liblo.send(target, "/ctrl", "lizzie2a", int(c))
            liblo.send(target, "/ctrl", "lizzie2b", float(d))
            print("Sending lizzie %i %f %i %f" % (int(a), float(b), int(c), float(d)))
            continue

        m = re.search("alex ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg) 
        if m:
            a = m.group(1)
            b = m.group(2)
            c = m.group(3)
            d = m.group(4)
            
            liblo.send(target, "/ctrl", "alex1a", int(a))
            liblo.send(target, "/ctrl", "alex1b", float(b))
            liblo.send(target, "/ctrl", "alex2a", int(c))
            liblo.send(target, "/ctrl", "alex2b", float(d))
            print("Sending alex %i %f %i %f" % (int(a), float(b), int(c), float(d)))
            # continue


#         m = re.search("carpet_list_bang ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
#         if m:
#             for i in range(0,13):
#                 print("Sending %s = %f" % ("carpet%d" % (i), float(m.group(i+1))))
#                 liblo.send(target, "/ctrl", ("carpet%d" % (i)), float(m.group(i+1)))
#             continue
        
#         m = re.search("hair_L ([0-9\.]+)", msg)
#         if m:
#             a = m.group(1)
# #            b = m.group(2)
            
#             liblo.send(target, "/ctrl", "hairL", float(a))
# #            print("Sending hairL %f" % (float(a)))
   
#         m = re.search("knee_D ([0-9\.]+) ([0-9\.]+)", msg)
#         if m:
#             a = m.group(1)
#             b = m.group(2)
            
#             liblo.send(target, "/ctrl", "kneeDa", float(a))
#             liblo.send(target, "/ctrl", "kneeDb", float(b))
#             print("Sending kneeD %f %f" % (float(a), float(b)))
    

       
