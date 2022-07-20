#!/usr/bin/python3
import zmq
import random
import time

xsub_addr = 'tcp://192.168.0.10:5556'
context = zmq.Context()
publisherSocket = context.socket(zmq.PUB)
publisherSocket.connect(xsub_addr)
publishName = b"rand"; #.encode('utf-8')

while True:
    f = str(random.random())
    msg = f.encode('utf-8')
    publisherSocket.send_multipart([publishName,msg])
    print(msg)
    time.sleep(0.025)
