from paho.mqtt import client as mqtt
import time

client = mqtt.Client("alex")

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected to MQTT Broker!")
  else:
    print("Failed to connect, return code %d\n", rc)

client.on_connect = on_connect

client.connect("localhost", 1883)

#client.loop_start()

def on_message(client, userdata, msg):
  print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

client.subscribe("xyz")
client.on_message = on_message

while True:
    client.loop(timeout=1.0,max_packets=10)

