#!/usr/bin/python3

import sys, pygame, math

import zmq, liblo, re, datetime, os, time

subnames = [b"face", b"hand", b"carpet_list", b"hair_L", b"hair_S", b"knee_J", b"knee_D", b"rand"]

context = zmq.Context()
subscriberSocket = context.socket(zmq.SUB)
subscriberSocket.connect('tcp://192.168.0.10:5555')

osc_target = liblo.Address("localhost", 6010)

half_pi = math.pi/2

segments = 16

tick = 0
cycle = 0
cps = 0.5625
cycletime = time.time()
values = {}

def cycle_now():
    delta = time.time() - cycletime
    return cycle + (cps * delta)

def tick_callback(path, args):
    global tick, cps, cycle, cycletime
    tick = args[0]
    cps = args[1]
    cycle = args[2]
    cycletime = time.time()
    #print("tick %d cps %f cycle %f" % (tick,cps,cycle))

def glove_callback(path, args):
    global tick, cps, cycle, cycletime
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
osc_server.add_method("/tick", "iff", tick_callback)

osc_server.add_method("/glove", "ffff", glove_callback)

osc_server.add_method(None, None, fallback)

for subname in subnames:
    subscriberSocket.setsockopt(zmq.SUBSCRIBE, subname)

pygame.init()
clock = pygame.time.Clock()

size = width, height = 1024, 768
midx = width/2
midy = height/2

white = 255, 255, 255
black = 0, 0, 0

cycles = 3
history = {}

screen = pygame.display.set_mode(size)

while 1:
    dt = clock.tick(20)
    # print(dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    now = cycle_now()

    #key = 'handosc'
    #key = 'rand'
    key = 'face'
    
    if key in history:
        # clear out old history
        for i in range(0,len(history[key])):
            (t, value) = history[key][i]
            #print("i: %d now: %f t: %f now - t: %f" % (i, now, t, now - t))
            if((now - t) < cycles):
                #if i > 0:
                    #print("bing")
                    # remove everything up to here
                #print(len(history[key]))
                history[key] = history[key][i:]
                #print(len(history[key]))
                break
        points = []

        # Draw line while calculating averages
        average_bins = []
        for i in range(0,segments):
            average_bins.append([])
            
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
        liblo.send(osc_target, "/ctrl", "facep", mini)        
        #print(averages)
        #print("seg %d len %d" % (segments, len(averages)))
        
        for i in range(0,segments):
            d = 300
            x = d * math.cos((i/segments)*math.tau-half_pi);
            y = d * math.sin((i/segments)*math.tau-half_pi);
            x2 = d * math.cos(((i+1)/segments)*math.tau-half_pi);
            y2 = d * math.sin(((i+1)/segments)*math.tau-half_pi);
            if ((i % segments) == (math.floor(now * 16) % 16)):
                colour = (255,255,255)
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
        
        m = re.search("face ([0-9\.]+) ([0-9\.]+) ([0-9\.]+) ([0-9\.]+)", msg)
        if m:
            name = "face"
            a = float(m.group(1))
            b = float(m.group(2))
            print("ah: " + str(a))
            if not name in history:
                history[name] = []
            history[name].append((now, a))
        if msg == 'rand':
            if not 'rand' in history:
                history['rand'] = []
            #print("rand %f" % (float(message[1])))
            history['rand'].append((now, float(message[1])))
            

        #print("name: %s msg: %s" % (name.decode("utf-8"), msg))
