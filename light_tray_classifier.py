#!/usr/bin/env python
# import publish
import threading
import subprocess
import adbutils
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import torch
from PIL import Image
from torchvision import transforms
from torchvision.transforms import ToTensor, Normalize

# Initialization
event = threading.Event()

# Start and connect to adb server
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(info.serial, info.state)

adb.connect('192.168.10.5:5555')
device = adb.device()
print(f"Connected to {device}")

device.shell(['input', 'keyevent', 'KEYCODE_CAMERA',
                            ';sleep', '0.1'])

print("Connecting to server")
ip = '192.168.10.5'
port = '5555'

# subprocess.call('adb')
# subprocess.call(['adb', 'start-server'])
# subprocess.call(['adb', 'tcpip', port])
# subprocess.call(['adb', 'connect', f'{ip}:{port}'])

# subprocess.call(['input', 'keyevent', 'KEYCODE_CAMERA'])
event.wait(1)

def main():
    pass


# Runs all the scripts we need in order to perform classification
if __name__ == "__main__":

    # Initialization for infinite loop
    running = True


    # Functions to make program work

    # Publishes to broker
    def start_publish(predicted):

        # This is the publisher
        client = mqtt.Client()
        client.connect('test.mosquitto.org', 1883, 60)

        # May need loop to iterate
        client.publish('tray_classification', predicted)


    # Subscibes to broker
    def start_subscribe():
        # May need a loop for continuous running
        print("Subscribe started")
        msg = subscribe.simple('tray_start', hostname='test.mosquitto.org')
        print(msg.payload.decode('utf-8'))


    # Opens camera app and takes pic
    def start_camera(device):
       # subprocess.check_output(['input', 'keyevent', 'KEYCODE_CAMERA',
       #                      ';sleep', '0.1'])
       device.shell(['input', 'keyevent', 'KEYCODE_CAMERA',
                     ';sleep', '0.1'])


    def classify_image(device):
        event.wait(5)
        pics = subprocess.check_output(['adb', 'shell', 'cd', '/storage/self/primary/DCIM/Camera', '; ls'])
        pics = pics.decode('utf-8')

        # Stores all image names in list to pull from
        image_list = []
        for image in pics.split('\n'):
            image_list.append(image)

        # Finds most recent image
        len_image_list = len(image_list)
        last_image = image_list[len_image_list-2]  # maybe change to -1
        print(f'Last image: {last_image}')

        # Pulls last image and stores to local directory
        origin_path = f'/storage/self/primary/DCIM/Camera/{last_image}'
        destination_path = '/app/images'
        subprocess.check_output(['adb', 'pull', origin_path, destination_path])
        print('Image pulled')
        # ----------------------------------------------------------------------------------------------------------------------
        # This script takes the last image and classifies it

        # Checks for GPU and loads model to it
        device = torch.device("cpu")
        print(device)

        model = torch.load('/app/jan28_Model.pth', map_location=device)
        model.eval()
        model.to(device)

        classes = [
            'correct',
            'incorrect'
        ]
        # Data augmentation and normalization for training
        # Just normalization for validation
        event.wait(1)

        # Finds last image in test directory to classify
        test_dir = '/app/images'
        # img_list = os.listdir(test_dir)
        print(f'Actual last image: {last_image}')
        img = Image.open(f'/app/images/{last_image}')

        # Image augmentation (same as model is trained on)
        transform = transforms.Compose([
            transforms.Resize(224),
            transforms.ColorJitter(brightness=(0.1, 0.6), contrast=1, saturation=0, hue=0.4),
            ToTensor(),
            Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Applies necessary transforms
        img = transform(img)
        img = img.unsqueeze(0)

        # Assigns classification to GPU
        image_tensor = img.cpu()
        print('To cpu')

        # Finds most probable class and prints result
        output = model(image_tensor)
        _, predicted = torch.max(output.data, 1)
        print(classes[predicted.item()])
        predicted = classes[predicted.item()]
        print(_)
        return predicted


    while running:
        try:
            # Script calls for program to work
            start_subscribe()  # Starts the mqtt subscribe script
            start_camera(device)  # Opens camera app
            predicted = classify_image(device)  # Classifies the new picture
            start_publish(predicted)
        except (RuntimeError, TypeError, NameError):
            print('Error')
            break
        else:
        # Script calls for program to work
            start_subscribe()  # Starts the mqtt subscribe script
            start_camera(device)  # Opens camera app
            predicted = classify_image(device)  # Classifies the new picture
            start_publish(predicted)
