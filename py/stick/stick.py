#!/usr/bin/python3

# (c) Alex Mclean, Lizzie Wilson and contributors
# Distributed under the terms of the GNU Public License version 3

import sys, pygame, math
import liblo, re, datetime, os, time, random
import linkclock


import zmq
subname = "stick"
addr = 'tcp://192.168.0.110:5555'

context = zmq.Context()

subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect(addr)
subscriberSocket.setsockopt_string(zmq.SUBSCRIBE, subname)

def cycle_now():
    return link_clock.cyclePos()

try:
    osc_server = liblo.Server(7070)
except liblo.ServerError as err:
    print(err)
    sys.exit()

osc_targets = [liblo.Address(6010), liblo.Address("192.168.0.104", 6010)]

fps = 40

pygame.init()
pygame_clock = pygame.time.Clock()

size = width, height = 1024, 1024
midx = width/2
midy = height/2

half_pi = math.pi/2

white = 255, 255, 255
black = 0, 0, 0
white = 255, 255, 255
yellow = 255, 255, 0

screen = pygame.display.set_mode(size)

history = []
segments = 16
history_cycles = 2
history_sz = segments * history_cycles


link_clock = linkclock.LinkClock(120, segments, 0)
link_clock.start()

received = False
received_t = 0

def simulate():
    global received,received_t
    if random.randrange(math.floor(fps*2)) == 0:
        received = True
        received_t = time.time()


max_weight = 0
for i in range(0,history_cycles):
    max_weight = max_weight + i + 1

prev = -1

pattern = []

for i in range(0,segments):
    pattern.append(0)

while 1:
    #simulate()

    dt = pygame_clock.tick(fps)
    t = link_clock.cyclePos()
    b = link_clock.beat()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    
    x = (300 * math.cos((t % 1)*math.tau-half_pi))+midx;
    y = (300 * math.sin((t % 1)*math.tau-half_pi))+midy;

    if subscriberSocket.poll(timeout=0):
        message = subscriberSocket.recv_multipart()
        print(message)
        msg = str(message[0]) #.decode("utf-8")
        if re.search(r"stick 1", msg):
            print("on")
            received = 1
        
    if received:
        if b != prev:
            history = list(filter(lambda x: (b - x) <= history_sz,history))
            history.append(b)
            prev = b
            print(history)
        
            for i in range(0,segments):
                pattern[i] = 0

            for h in history:
                pattern[h%segments] = pattern[h%segments] + (history_cycles-math.floor((b-h)/segments))
        
        print(pattern)

        mini = " ".join(map(str, pattern))
        print("mini: ", mini)
        for osc_target in osc_targets:
            liblo.send(osc_target, "/ctrl", "stick", mini)
        
        received = False
    
    sz = 40 - (min(time.time()-received_t,0.25)*100)

    for i in range(0,segments):
        value = pattern[i]
        if value > 0:
            d = 300
            xa = d * math.cos((i/segments)*math.tau-half_pi);
            ya = d * math.sin((i/segments)*math.tau-half_pi);
            xb = d * math.cos(((i+1)/segments)*math.tau-half_pi);
            yb = d * math.sin(((i+1)/segments)*math.tau-half_pi);
            channel = 108+(147*(value/max_weight))
            colour = channel, channel, 0
            pygame.draw.polygon(screen, colour, ((xa+midx,ya+midy),
                                                 (xb+midx,yb+midy),
                                                 (midx,midy),
                                                 )
                                )
        
    
    if (time.time()-received_t) > 0.25:
        c = white
    else:
        c = yellow

    pygame.draw.circle(screen, c, (x, y), sz)
    pygame.display.flip()

        
