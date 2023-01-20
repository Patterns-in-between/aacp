#!/usr/bin/python3

# (c) Alex Mclean, Lizzie Wilson and contributors
# Distributed under the terms of the GNU Public License version 3

import sys, pygame, math

import zmq, liblo, re, datetime, os, time

from scipy.signal import find_peaks

import linkclock

import statistics

#subnames = [b"textile1", b"textile2", b"textile3"]
subnames = [b"ml"]

context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)

# 192.168.0.10 is the raspberry pi
subscriberSocket.connect('tcp://192.168.0.10:5555')
# subscriberSocket.connect('tcp://127.0.0.1:5555')

samplerate = 25 # TODO - calculate this

osc_target = liblo.Address("localhost", 6010)

half_pi = math.pi/2

segments = 16

peak_segments = 16

tick = 0
cycle = 0
cps = 0.5625
#cycletime = time.time()
values = {}

link_clock = linkclock.LinkClock(120, 4, 0)
link_clock.start()

def cycle_now():
    # delta = time.time() - cycletime
    #return cycle + (cps * delta)
    return link_clock.cyclePos()

# def tick_callback(path, args):
#     global tick, cps, cycle, cycletime
#     tick = args[0]
#     cps = args[1]
#     cycle = args[2]
#     cycletime = time.time()
#     #print("tick %d cps %f cycle %f" % (tick,cps,cycle))

def glove_callback(path, args):
    now = cycle_now()
    if not "handosc" in history:
        history["handosc"] = []
    value = (args[0] - 0.2) * 2.5
    
    history['handosc'].append((now, value))

def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))

try:
    osc_server = liblo.Server(1234)
except liblo.ServerError as err:
    print(err)
    sys.exit()

# Using link sync now
# osc_server.add_method("/tick", "iff", tick_callback)

osc_server.add_method("/glove", "ffff", glove_callback)

osc_server.add_method(None, None, fallback)

for subname in subnames:
    subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)

pygame.init()
pygame_clock = pygame.time.Clock()

size = width, height = 1024, 768
midx = width/2
midy = height/2

white = 255, 255, 255
black = 0, 0, 0

cycles = 2
history = {}

screen = pygame.display.set_mode(size)

while 1:
    dt = pygame_clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    now = cycle_now()

    #key = 'handosc'
    #key = 'rand'
    #key = 'face'
    key = 'ml'
    
    if key in history:
        # clear out old history
        for i in range(0,len(history[key])):
            (t, value) = history[key][i]
            if((now - t) < cycles):
                history[key] = history[key][i:]
                break
        
        points = []

        # Draw line while calculating averages
        average_bins = []
        for i in range(0,segments):
            average_bins.append([])

        # Find peaks for values
        peaks = find_peaks([row[1] for row in history[key]],
                           distance = samplerate/3, # peaks at least 1/3 a second apart ?
                           width = samplerate/8, # peaks at least 1/8 of a second 'wide' ?
                           #prominence=(None, 0.6)
                           )[0]
        
        def to_cycle_and_value(i):
            return ((history[key][i][0]) % 1, history[key][i][1])
        
        peak_t = list(map(to_cycle_and_value, peaks))
        peak_t.sort()

        # filter out small peaks
        peak_t = list(filter(lambda x: x[1] > 0.1, peak_t))

        
        for (t, value) in history[key]:
            #print("t: %f, value: %f" % (t, value))
            x = (value * 300 * math.cos((t % 1)*math.tau-half_pi))+midx;
            y = (value * 300 * math.sin((t % 1)*math.tau-half_pi))+midy;
            points.append((x,y))
            #print("%fx%f" % (x,y))
            segment = math.floor(t * segments) % segments
            #print("seg: %d" %  (segment,))
            average_bins[segment].append(value)

        averages = []
        for i in range(0, segments):
            c = len(average_bins[i])
            if c > 0:
                s = sum(average_bins[i])
                averages.append(s/c)
                #print(average_bins[i])
                #print("avg: %f" %  (a/c,))
            else:
                averages.append(0)
        mini = " ".join(map(str, averages))
        liblo.send(osc_target, "/ctrl", "ml", mini)
        #print(mini)
        #print(averages)
        #print("seg %d len %d" % (segments, len(averages)))

        peak_bin_bools = [False] * peak_segments
        
        if len(peak_t) > 0:
            # quantise the peaks
            peak_bins = []
            for i in range(0, peak_segments):
                peak_bins.append([])
            for x in peak_t:
                pos, val = x
                peak_bin = math.floor(pos * peak_segments)
                print("peak in bin %d from pos %.2f" % (peak_bin, pos))
                peak_bins[peak_bin].append(val)
                peak_bin_bools[peak_bin] = True

            peak_bin_mini = []
            for i in range(0, peak_segments):
                if len(peak_bins[i]) == 0:
                    peak_bin_mini.append("~")
                else:
                    peak_bin_mini.append("%.4f" % statistics.mean(peak_bins[i]))

            print(" ".join(peak_bin_mini))
            liblo.send(osc_target, "/ctrl", "peakbins", " ".join(peak_bin_mini))
        else:
            liblo.send(osc_target, "/ctrl", "peakbins", " ")
        
        for i in range(0,segments):
            d = 300
            x = d * math.cos((i/segments)*math.tau-half_pi);
            y = d * math.sin((i/segments)*math.tau-half_pi);
            x2 = d * math.cos(((i+1)/segments)*math.tau-half_pi);
            y2 = d * math.sin(((i+1)/segments)*math.tau-half_pi);
            if ((i % segments) == (math.floor(now * segments) % segments)):
                colour = (255,255,255)
            else:
                if (peak_bin_bools[i % peak_segments]):
                    colour = (128,128,255)
                else:
                    colour = (128,128,128)
            # pygame.draw.circle(screen, white, (x+(width/2),y+(height/2)), 10)
            w = 1 + (averages[i]/2)
            pygame.draw.polygon(screen, colour, ((x+midx,y+midy),
                                                 (x2+midx,y2+midy),
                                                 (x2*w+midx,y2*w+midy),
                                                 (x*w+midx,y*w+midy),
                                                 )
                                )
        #print("points: %d"%  (len(points)))
        if len(points) > 1:
            pygame.draw.lines(screen, (255,255,255), False, points, 4)
            
        if len(peak_t) > 0:
            # turn peak times into a list of durations with values,
            # drawing the peaks as circles as we go..
            peak_durs = []
            peak_durs.append((peak_t[0][0], None))
            
            for i, x in enumerate(peak_t):
                (p, val) = x

                x = (val * 300 * math.cos((p%1)*math.tau-half_pi))+midx;
                y = (val * 300 * math.sin((p%1)*math.tau-half_pi))+midy;
                
                pygame.draw.circle(screen, (255,128,128), (x,y), 5)
                
                if i < (len(peak_t) - 1):
                    dur = peak_t[i+1][0] - p
                else:
                    dur = 1 - p
                peak_durs.append((dur, val))

            # construct mini-notation string
            peak_mini = []
            for dur, val in peak_durs:
                if val == None:
                    peak_mini.append("~@%.4f" % max(dur, 0.0001)) # avoid 0 durations!
                else:
                    peak_mini.append("%.4f@%.4f" % (val, max(dur, 0.0001)))
            joined_mini = " ".join(peak_mini)
            print(joined_mini)
            liblo.send(osc_target, "/ctrl", "peaks", joined_mini)
            
    # pygame.draw.rect(screen, white, (100,100,200,200))
    #pygame.draw.polygon(screen, white, ((100,100),(200,200),(300,100)))

    pygame.display.flip()
    osc_server.recv(0)    
    while subscriberSocket.poll(timeout=1):
        message = subscriberSocket.recv_multipart()
        msg = str(message[0]) #.decode("utf-8")
        #print(message)
        msg = re.sub(r"^b'","",msg)
        msg = re.sub(r";.*$","",msg)
        msg = re.sub(r"'$","",msg)

        now = cycle_now()
        
        m = re.search("ml ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            name = "ml"
            #print("match")
            a = float(m.group(1))
            b = float(m.group(2))
            c = float(m.group(3))
            d = float(m.group(4))
            #print("ah: " + str(a))
            if not name in history:
                history[name] = []
            history[name].append((now, b))
        if msg == 'rand':
            if not 'rand' in history:
                history['rand'] = []
            #print("rand %f" % (float(message[1])))
            history['rand'].append((now, float(message[1])))
            

        #print("name: %s msg: %s" % (name.decode("utf-8"), msg))
