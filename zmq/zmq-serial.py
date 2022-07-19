#!/usr/bin/python3

import zmq
import serial
import re

ser = serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_5573731323135141A191-if00", 115200, timeout=1) 

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.0.10:5555")

socket.setsockopt(zmq.SUBSCRIBE, b"red")
socket.setsockopt(zmq.SUBSCRIBE, b"green")
socket.setsockopt(zmq.SUBSCRIBE, b"blue")
socket.setsockopt(zmq.SUBSCRIBE, b"light")
socket.setsockopt(zmq.SUBSCRIBE, b"carpet")

while True:
    if socket.poll(timeout=1000):
        message = socket.recv_multipart()

        msg = str(message[0]) #.decode("utf-8")
        msg = re.sub(r"^b'","",msg)
        msg = re.sub(r";.*$","",msg)

        #print(message)
        if (message[0] == b'red'):
            ser.write(message[1] + b'r')
        if (message[0] == b'green'):
            ser.write(message[1] + b'g')
        if (message[0] == b'blue'):
            ser.write(message[1] + b'b')
        if (message[0] == b'light'):
            ser.write(message[1] + b'x')
        m = re.search("carpet ([0-9\.]+) ([0-9\.]+)", msg)
        if (m):
           # print(str(int(float(m.group(1))*256)) + 'x')
            ser.write(str.encode(str(int(float(m.group(1))*256))) + b'x')
