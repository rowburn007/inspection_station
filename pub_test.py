import time

import paho.mqtt.client as mqtt

def on_publish(client, userdata, message):
    print("published")

# Define MQTT Broker and Credentials
broker = "test.mosquitto.org"
port = 1883
username = "tray-classifier"
passwd = "futurefactories"

# Define Topic and Message
topic = "tray"

# Create MQTT Client
mqtt = mqtt.Client()

# Set Credentials
mqtt.username_pw_set(username, password=passwd)

mqtt.on_publish = on_publish

# Connect to MQTT Broker
mqtt.connect(broker, port)
mqtt.loop_start()
# Publish Message to Topic

# Disconnect from MQTT Broker
# client.disconnect()
while True:
    msg = 1
    time.sleep(0.5)
    mqtt.publish(topic, msg)