import paho.mqtt.client as mqtt

# Define MQTT Broker and Credentials
broker = "test.mosquitto.org"
port = 1883
username = "tray-classifier"
passwd = "futurefactories"

# Define Topic
topic = "tray"

def on_subscribe(client, userdata, rc, qos):
    print(f"Subscribed with code {rc}")
# Define Callback Function to Process Received Messages
def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))

def on_connect(client, userdata, flag, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Could not connect, rc = {rc}")
# Create MQTT Client
mqtt = mqtt.Client()
# Set Credentials
mqtt.username_pw_set(username, password=passwd)
mqtt.on_subscribe = on_subscribe

# Connect to MQTT Broker
mqtt.on_connect = on_connect
mqtt.connect(broker, port)
mqtt.subscribe(topic)
mqtt.on_message = on_message

mqtt.loop_forever()