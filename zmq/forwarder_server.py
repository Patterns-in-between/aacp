#!/usr/bin/python

import zmq
import random
import sys
import time

server = "slab.org"
port = "5559"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://%s:%s" % (server,port))
publisher_id = random.randrange(0,9999)
while True:
    topic = random.randrange(1,10)
    messagedata = "server#%s" % publisher_id
    print "%s %s" % (topic, messagedata)
    socket.send("%d %s" % (topic, messagedata))
    time.sleep(1)
