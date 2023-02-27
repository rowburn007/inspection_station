
def main():
    pass


def start_publish():
    import paho.mqtt.client as mqtt

    # This is the publisher
    client = mqtt.Client()
    client.connect('test.mosquitto.org', 1883, 60)

    num = 2
    client.publish('tray_start', num)


if __name__ == '__main__':
    start_publish()
