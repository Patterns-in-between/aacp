### Using the DJTelloPy library to control the Tello Drone 
## Receive OSC from Tidalcycles on port 6669 (creating an osc target in Haskell)


from __future__ import print_function
import liblo, sys

from djitellopy import Tello


# ## Send tello commands  
tello = Tello()

tello.connect()
tello.takeoff()


delay(500)

# # print(tello.get_acceleration_x())

# tello.move_left(20)
# # tello.flip_left()
# tello.move_right(20)


# tello.land()

# create server, listening on port 6669
try:
    server = liblo.Server(6669)
except liblo.ServerError as err:
    print(err)
    sys.exit()

def foo_bar_callback(path, args):
    i, f = args
    print("received message '%s' with arguments '%d' and '%f'" % (path, i, f))

def foo_baz_callback(path, args, types, src, data):
    print("received message '%s'" % path)
    print("blob contains %d bytes, user data was '%s'" % (len(args[0]), data))

def fallback(path, args, types, src):
    # if ( args > 1):
    #     print("done")
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print(a)
        if (a >= 0.5):
            # print("done")
            tello.move_left(20)
            # print("argument of type '%s': %s" % (t, a))
        if (a > 0.0 and a < 0.5 ):
            tello.move_right(20)
        if (a == 0.0): 
            tello.land()

# register method taking an int and a float
server.add_method("/foo/bar", 'if', foo_bar_callback)

# register method taking a blob, and passing user data to the callback
server.add_method("/foo/baz", 'b', foo_baz_callback, "blah")

# register a fallback for unhandled messages
server.add_method(None, None, fallback)

# loop and dispatch messages every 100ms
while True:
    server.recv(100)