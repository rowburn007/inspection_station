
def main():
    pass


def start_publish():
    import paho.mqtt.client as mqtt
    import random
    import time

    # This is the publisher
    client = mqtt.Client()
    client.connect('test.mosquitto.org', 1883, 60)

    while True:
        num = random.randint(1, 101)
        client.publish('random_number', num)
        time.sleep(5)


if __name__ == '__main__':
    start_publish()
