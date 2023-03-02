# subscirbe script
def main():
    pass


def start_subscribe():
    import paho.mqtt.subscribe as subscribe

    # May need a loop for continuous running
    while True:
        msg = subscribe.simple('tray_classification', hostname='test.mosquitto.org')
        print(msg.payload.decode('utf-8'))


if __name__ == '__main__':
    start_subscribe()

