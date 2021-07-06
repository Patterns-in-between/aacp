#!/usr/bin/env python3

import liblo, sys, re, datetime, os, time
from espeakng import ESpeakNG

#except liblo.ServerError as err:
#    print(err)
#    sys.exit()

server = liblo.Server(6050)

e = ESpeakNG()

#e.audio_dev = "jack"

def espeak_callback(path, args):
    word, e.voice, e.pitch, e.speed = args
    print(word)
    e.say(word)

def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))

# word, voice, pitch, speed

server.add_method("/espeak", 'ssff', espeak_callback)

server.add_method(None, None, fallback)

while True:
    server.recv(100)
