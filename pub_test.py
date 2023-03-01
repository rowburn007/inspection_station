# import paho.mqtt.client as mqtt
# import time
#
# def on_log(client, userdata, level, buf):
#     print(f"log: {buf}")
#
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected!")
#     else:
#         print(f"Bad connection returned code = {rc}")
#
# def on_disconnect(client, userdata, flags, rc=0):
#     print(f"Disconnected, result code = {str(rc)}")
#
#
# broker= "test.mosquitto.org"
# port = 1883
#
# client = mqtt.Client("Classification-Station") # Creating new instance
# client.on_connect = on_connect
# # client.on_log = on_log
# client.on_disconnect = on_disconnect
#
#
# print(f"Connecting to broker : {broker}")
# client.connect(broker, port=port)  # Connects to broker
#
# client.loop_start()  # Start loop
# client.publish("tray-detection", "detected")  # Publishes to topic tray-detection
# time.sleep(4)
# client.loop_stop()  # End loop
#
# client.disconnect()  # Disconnects

import paho.mqtt.client as mqtt


def on_publish(client, userdata, message):
    print("published")

# Define MQTT Broker and Credentials
broker_address = "test.mosquitto.org"
username = "tray-classifier"
password = "futurefactories"

# Define Topic and Message
topic = "tray"
message = "1"

# Create MQTT Client
client = mqtt.Client()

# Set Credentials
client.username_pw_set(username, password)

client.on_publish = on_publish

# Connect to MQTT Broker
client.connect(broker_address, port=1883)

# Publish Message to Topic
client.publish(topic, message)

# Disconnect from MQTT Broker
client.disconnect()