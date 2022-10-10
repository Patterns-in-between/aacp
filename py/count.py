#!/usr/bin/python3

# (c) Alex Mclean, Lizzie Wilson and contributors
# Distributed under the terms of the GNU Public License version 3

import zmq, liblo, re, datetime, os, time

subnames = ["deva", "juan", "lizzie", "alex"]

context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)

# for glove simulation
try:
    osc_server = liblo.ServerThread(6060)
    print("hmm")
except liblo.ServerError as err:
    print(err)
    sys.exit()

people = {}
threshold = 0.5
digits = 5

# 192.168.0.10 is the raspberry pi
# subscriberSocket.connect('tcp://192.168.0.10:5555')
subscriberSocket.connect('tcp://127.0.0.1:5555')

person_id = 1
for subname in subnames:
    subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname.encode("ASCII"))
    people[subname] = {'count': 0,
                       'open': False,
                       'last': 0,
                       'id': person_id
                      }
    person_id += 1

superdirt = liblo.Address("localhost", 57120)
superbus  = liblo.Address("localhost", 57110)


def incoming(name, a, b, c, d):
    person = people[name]
    # use the fourth number for now!
    value = d
    print(d)
    if not person['open']:
        if value > threshold:
            person['open'] = True
            print("trigger")
            # trigger sound
            message = [
                's', 'aacpcount',
                'n', person['count'] % digits,
                'speed', 1,
                'amp', ("c%d" % person['id'])
            ]
            person['count'] += 1
            liblo.send(superdirt, "/dirt/play", *message)

    if person['open']:
        if value < threshold:
            person['open'] = False
            # liblo.send(superbus, "/c_set", person['id'], 0)            
#        else:
#
    liblo.send(superbus, "/c_set", person['id'], value)

def glove_callback(path, args):
    print("hmm!")
    print("incoming %f %f %f %f" % tuple(args))
    incoming("alex", *args)
    return False

def default_callback(path, args):
    print("unknown path: %s" % path)
          
osc_server.add_method("/ctrl", "ffff", glove_callback)
osc_server.add_method(None, None, default_callback)
osc_server.start()

while True:
    if subscriberSocket.poll(timeout=1000):
        message = subscriberSocket.recv_multipart()
        msg = str(message[0]) #.decode("utf-8")
        msg = re.sub(r"^b'","",msg)
        msg = re.sub(r";.*$","",msg)
        
        m = re.search("(deva|juan|lizzie|alex) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            name = m.group(1)
            a = m.group(2)
            b = m.group(3)
            c = m.group(4)
            d = m.group(5)
            incoming(name, a, b, c, d)
            continue
