# inspection_station
Introduction

	The goal of this project is to create a custom visual inspection system for use in the Future Factories rocket assembly process. Visual inspection is a critical component for quality and process control in the manufacturing industry specifically as we push towards industry 4.0. The goal of the Future Factories lab is to research manufacturing techniques which will push us closer towards industry 4.0. Industry 4.0 is full cyber-physical integration into the manufacturing process. Visual inspection is one key piece of this puzzle which allows the manufacturing cell to see and interpret what is going on through computer vision. By the end of this project a fully autonomous visual inspection station should be built which correctly categorizes and communicates the result of a parts tray it is presented with. By completing this project I will have gained valuable knowledge and experience in the world of ai and computer lesion as well as IIOT. 

Methods

The Phone:

Visual Inspection stations utilizing mobile phones have been deployed within the Future Factories lab before. Previously, IPhones running IBM Maximo software were used for visual inspection (VI). While IBM's Maximo is very powerful and easy to implement, it is expensive and proprietary software. This proprietary nature does not lend itself to tinkering and open modifications. Features which are critical for learning and research. This project serves to create a new platform for students to develop and implement mobile VI systems. The android phone is the key to this all. The new VI station makes use of a rooted android phone. Which is simply an android phone that has been "unlocked" or "rooted", thus giving the user unrestricted internal access to the phone. Access that is crucial for software development, and is unachievable on IPhones. The rooted phone contains all the necessary hardware and software to perform image classification. The phone is able to communicate over the network using MQTT, take and store pictures using the embedded camera and internal storage. Image classification is performed using the phone's internal processor.

The Visual Inspection Model:

	Currently, the visual inspection station makes use of a rooted android cell phone for capturing, storing, and classifying the inspection images. The image classification model was trained using PyTorch and resnet18 as its pre-trained convolutional base. A custom image binary classifier is added on top of the frozen convolutional base. This custom classifier takes an input rocket tray image, and classifies it as either ‘correct’ or ‘incorrect’. The model was fed 3,000 images of various red and garnet part/tray configurations. 50% correct and 50% incorrect. The model was then trained on the dataset with a standard 80/20 training/validation split For this classification task, proper data augmentation was crucial for generating accurate predictions. Specifically, any image flip or rotation augmentations had to be omitted since tray orientation matters. Also, random color and saturation shifts were applied to the augmented data in order to account for variance in scene lighting and part color. Several models were trained using different training and data augmentation techniques. Training was also performed on several different image datasets, consisting of different image capture angles and tray configurations. Each successive model was saved and named as the date it was trained on. The most accurate model was kept for deployment. The result was a binary image classification model saved as jan_28model.pth which is capable of discerning correct and incorrect part variations in images taken from top down orthographic view points. This model is highly accurate when images are taken from the current camera mounting position, just above the first manufacturing station. The model can also accurately make predictions on tray/part combinations with different colors than the ones it was trained on.


Docker Implementation:

To deploy the VI model on the android phone, a Docker container was utilized. A Docker container is simply a unit of software that packages code and its dependencies so the application runs quickly and reliably across computing environments [1]. For this project Docker was utilized to simplify the implementation of python code/libraries within the android operating system. Containers allow the code to run as if it is on its own Linux machine. This prevents hardware and software conflicts from occurring when deploying between different systems. The VI code and the PyTorch model file were packaged together using a Dockerfile and built within the rooted android phones file system. The code can then be executed by running the Docker container.
	

MQTT Implementation

MQTT is a common communication protocol within the manufacturing industry. It utilizes a client/broker system where the broker acts as a middle man for distributing data. MQTT allows various systems across a network to subscribe to certain topics in order to receive information. Clients can also publish information to the broker for other clients to subscribe to. MQTT communication is necessary for allowing the VI station to communicate with other clients on the network. In the Future Factories manufacturing cell, integration with Siemens PLCs is critical for the station to operate as designed. During operation, the VI station is triggered whenever a parts tray is detected by the first tray station. At this location, the proximity sensor is connected to a PLC which publishes the value to the corresponding topic on the lab’s MQTT broker. The Docker container within the phone contains an MQTT client which is subscribed to this topic. Once a new value is published to this topic, the VI code is run to classify the tray. This code takes a picture, stores the image, pulls the image into the docker container, classifies the image, and finally publishes the predicted class to a new MQTT topic. From there the automation system will decide whether to continue or stop the process based on the classification result. Without this MQTT communication, none of the parts of the manufacturing process would be able to communicate with each other and autonomy would not be possible.



Quick start instructions

Mount phone in VI station mount with forward-facing camera in the top position.
Ensure the phone is connected to the same network as the MQTT broker.
Ensure the phones ip has not changed from 192.168.10.5
Select the VI application.
Trigger station with tray.



Documentation
Phone Overview

	The phone is a Samsung Galaxy XCover6 Pro. Its serial number is (R3CT30RZ2HL). The serial number is important for USB debugging. All VI files are located in the ‘/Docker’ directory (/storage/self/primary/Docker). A bash script is used to automatically start the docker container (/data/var/user/android-run-tc.sh). All images taken by the front facing camera are automatically stored in the ‘/Camera’ directory (/storage/self/primary/DCIM/Camera).

Model Overview

	For visual inspection, a binary image classification model was trained using PyTorch. The bulk of the feature extraction is achieved by the pretrained convolutional base (resnet18). For tray classification, a custom image classifier was added on top of the pretrained base. For training, training image files were split into two directories, one for each class (‘correct’ & ‘incorrect’). Within each class are the train and validation directories (‘train’ & ‘val’). To expand the model and train on new images, simply copy new images into their respective directories (maintaining 80/20 split) and retrain the model.


Code Overview

Fig. 1 High level program architecture
	
	The code needed to control this whole program is stored in two files ‘light_tray_classifier.py’ and ‘jan28_Model.pth’. The file ‘light_tray_classifier.py’ handles starting the following:

Starting and connecting to the adb server
Subscribing to the MQTT broker
Taking picture
Moving image files to container
Classifying image files
Publishing results

The file ‘jan28_Model.pth’ contains the PyTorch image classification model. This model is referenced by ‘light_tray_classifier.py’ (Fig. 2).

Fig. 2 Detailed program architecture
All functions referenced within the code are stored in individual functions. These functions are called successively within an infinite run loop. This infinite loop pauses on the start_subscribe() function which listens for incoming MQTT messages. The message is sent through the (start_tray) topic, referencing that a tray has been detected. Once a MQTT message is received the whole program iterates once and publishes the classification result to the broker. The program then pauses on the start_subscribe() function until another tray is detected.

Docker Overview

	The whole tray_classification program runs in a standalone docker container (tray-classifier). The image is stored in a docker repository as ‘rowburn007/tray-classifier’. However, for best results, the docker image was built on the android device. This was done to avoid conflicts with differing system architectures between laptop and android phone. Ideally with docker, system architecture should not matter. This can be fixed in future iterations. To build the docker file with native android support, use adb push to copy the necessary files to the Docker directory within the android phone. 

Push the following files:
Dockerfile
.dockerignore
requirements.txt
light_tray_classifier.py
jan28_Model.pth

Build the image with ( docker build -t tray-classifier . ). Once the image is built, run it with  docker run -it tray-classifier ). Alternatively, the docker container can be run using the shell script ( ./data/var/user/android-run-tc.sh ).

MQTT Overview

	This project makes use of paho-mqtt for its python MQTT  implementation. The publish and subscribe operations are split into two functions ‘start_publish()’ and ‘start_subscribe()’. Each function publishes/subscribes to a different topic. The start_subscribe() function listens to the topic ‘start_tray’ which is triggered when a new tray is detected within the station. 
