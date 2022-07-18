#!/usr/bin/python3

import zmq
import serial
ser = serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_5573731323135141A191-if00", 115200, timeout=1) 

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.0.10:5555")

socket.setsockopt(zmq.SUBSCRIBE, b"red")
socket.setsockopt(zmq.SUBSCRIBE, b"green")
socket.setsockopt(zmq.SUBSCRIBE, b"blue")
socket.setsockopt(zmq.SUBSCRIBE, b"light")

while True:
    if socket.poll(timeout=1000):
        message = socket.recv_multipart()
        print(message)
        if (message[0] == b'red'):
            ser.write(message[1] + b'r')
        if (message[0] == b'green'):
            ser.write(message[1] + b'g')
        if (message[0] == b'blue'):
            ser.write(message[1] + b'b')
        if (message[0] == b'light'):
            ser.write(message[1] + b'x')
