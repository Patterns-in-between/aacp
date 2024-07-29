import utime as time
from pimoroni_i2c import PimoroniI2C
from breakout_msa301 import BreakoutMSA301
import network
import socket
import machine

led = machine.Pin("LED", machine.Pin.OUT)

try:
    from ustruct import pack
except ImportError:
    from struct import pack

if isinstance('', bytes):
    have_bytes = False
    unicodetype = unicode  # noqa
else:
    have_bytes = True
    unicodetype = str

friend = "192.168.0.105"
osc_port = 7070

#from umqtt.simple import MQTTClient

#from pythonosc import udp_client

#wlan=network.WLAN(network.STA_IF)
#wlan.active(True)

# Connect to network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#print("scanning...")
#accesspoints = wlan.scan()
#for ap in accesspoints:
#        print(ap)
wlan.connect("alpacalab","dorkface")

# Wait for connect or fail
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    print('IP: ', wlan.ifconfig()[0])

so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = socket.getaddrinfo(friend, osc_port)[0][-1]

print('destination:', dest)

def pack_string(s, encoding='utf-8'):
    """Pack a string into a binary OSC string."""
    if isinstance(s, unicodetype):
        s = s.encode(encoding)
    assert all((i if have_bytes else ord(i)) < 128 for i in s), (
        "OSC strings may only contain ASCII chars.")

    slen = len(s)
    return s + b'\0' * (((slen + 4) & ~0x03) - slen)


def send_osc(x,y,z):
    data = pack('>f', x) + pack('>f', y) + pack('>f', z)
    msg = pack_string("/alex") + pack_string(",fff") + data
    #print(msg)
    so.sendto(msg, dest)

#client = MQTTClient("pipico", "192.168.0.103", keepalive=3600)
#client.connect()

# import mip
# mip.install("micropython-osc")

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA301(i2c)

part_id = msa.part_id()
print("Found MSA301. Part ID: 0x", '{:02x}'.format(part_id), sep="")

msa.enable_interrupts(BreakoutMSA301.FREEFALL | BreakoutMSA301.ORIENTATION)

prevx = 0
prevy = 0
prevz = 0

mx = 0.2

while True:
    x = msa.get_x_axis()
    y = msa.get_y_axis()
    z = msa.get_z_axis()

    if abs(x - prevx) < mx and abs(y - prevy) < mx and abs(z - prevz) < mx :
        led.off()
    else:
        led.on()
    #print("X:", x, end=",\t")
    #print("Y:", y, end=",\t")
    #print("Z:", z, end=",\t")
    #print("Freefall?", msa.read_interrupt(BreakoutMSA301.FREEFALL), end=",\t")
    #print("Orientation:", msa.get_orientation())
    #client.publish("xyz", "%f %f %f" % (msa.get_x_axis(),msa.get_y_axis(),msa.get_z_axis()), True)
    send_osc(msa.get_x_axis(),msa.get_y_axis(),msa.get_z_axis())
    time.sleep(0.05)
    prevx = x
    prevy = y
    prevz = z
