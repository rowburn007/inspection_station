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