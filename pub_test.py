import paho.mqtt.client as mqtt

def on_publish(client, userdata, message):
    print("published")

# Define MQTT Broker and Credentials
broker_address = "test.mosquitto.org"
# username = "tray-classifier"
# password = "futurefactories"

# Define Topic and Message
topic = "tray"
message = "1"

# Create MQTT Client
client = mqtt.Client()

# Set Credentials
# client.username_pw_set(username, password)

client.on_publish = on_publish

# Connect to MQTT Broker
client.connect(broker_address, port=1883)

# Publish Message to Topic
client.publish(topic, message)

# Disconnect from MQTT Broker
client.disconnect()