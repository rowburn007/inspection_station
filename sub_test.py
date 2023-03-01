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
# def on_message(client, userdata, msg):
#     topic = msg.topic
#     msg_decode = str(msg.payload.decode("utf-8"))
#     print(f"Message recieved: {msg_decode}")
#
#
# broker = "test.mosquitto.org"
# port = 1883
#
# client = mqtt.Client("Classification-Station") # Creating new instance
# client.on_connect = on_connect
# # client.on_log = on_log
# client.on_message = on_message
# client.on_disconnect = on_disconnect
#
#
# print(f"Connecting to broker : {broker}")
# client.connect(broker, port=port)  # Connects to broker
#
# client.publish("tray-detection", "detected")  # Publishes to topic tray-detection
# # time.sleep(4)
# client.loop_forever()  # End loop

# client.disconnect()  # Disconnects
import paho.mqtt.client as mqtt

# Define MQTT Broker and Credentials
broker_address = "test.mosquitto.org"
# username = "tray-classifier"
# password = "futurefactories"

# Define Topic
topic = "tray"

def on_subscribe(client, userdata, rc, qos):
    print(f"Subscribed with code {rc}")
# Define Callback Function to Process Received Messages
def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))

# Create MQTT Client
client = mqtt.Client()

client.on_subscribe = on_subscribe
# Set Credentials
# client.username_pw_set(username, password)

# Connect to MQTT Broker
client.connect(broker_address, port=1883, keepalive=60)
# Subscribe to Topic
client.subscribe(topic)

# Set Callback Function for Received Messages
client.on_message = on_message

# Start Background Thread for Incoming Messages
client.loop_start()

# Keep Main Thread Running to Receive Messages
while True:
    pass