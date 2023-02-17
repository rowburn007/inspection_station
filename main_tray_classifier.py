# import publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import subprocess
import torch
import os
from torchvision import transforms
from PIL import Image
from torchvision.transforms import ToTensor, Normalize
import time

def main():
    pass


# Runs all the scripts we need in order to perform classification
if __name__ == "__main__":

    # Functions to make program work
    # Checks if device is connected and starts server if not
    def connect_device():
        connected_devices = str(subprocess.check_output(['adb', 'devices']))
        if connected_devices.count('192.168') >= 0:
            pass
        else:
            start_server()

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
        msg = subscribe.simple('random_number', hostname='test.mosquitto.org')
        print(msg.payload.decode('utf-8'))

    # Starts adb serer
    def start_server():
        print("Connecting to server")
        ip = '192.168.10.5'
        port = '5555'

        subprocess.call('adb')
        subprocess.call(['adb', 'start-server'])
        subprocess.call(['adb', 'tcpip', port])
        subprocess.call(['adb', 'connect', f'{ip}:{port}'])

    # Opens Camera app to get ready to take pic
    def start_camera():
        subprocess.call(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_CAMERA'])
        time.sleep(1)

    # Takes a picture
    def take_pic():
        subprocess.call(['adb', 'shell', "am start -a android.media.action.STILL_IMAGE_CAPTURE",
                         ';input', 'keyevent', 'KEYCODE_FOCUS',
                         ';sleep', '1',
                         ';input', 'keyevent', 'KEYCODE_CAMERA',
                         ';sleep', '2'])

    def classify_image():
        pics = subprocess.check_output(['adb', 'shell', 'cd', '/storage/self/primary/DCIM/Camera', '; ls'])
        pics = pics.decode('utf-8')

        # Stores all image names in list to pull from
        image_list = []
        for image in pics.split('\n'):
            image_list.append(image)

        # Finds most recent image
        list_Length = len(image_list)
        last_image = image_list[list_Length - 1]
        print(f'Last image: {last_image}')

        # Pulls last image and stores to local directory
        origin_path = f'/storage/self/primary/DCIM/Camera/{last_image}'
        destination_path = '/app/images'
        subprocess.check_output(['adb', 'pull', origin_path, destination_path])
        time.sleep(1)
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

        # Finda last image in test directory to classify
        test_dir = '/app/images'
        img_list = os.listdir(test_dir)
        time.sleep(3)
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


    # Script calls for program to work
    start_subscribe()  # Starts the mqtt subscribe script
    connect_device()  # Connects to device
    # start_camera()  # Opens camera app
    take_pic()  # Takes one picture
    predicted = classify_image()  # Classifies the new picture
    start_publish(predicted)
