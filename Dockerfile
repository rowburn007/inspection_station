FROM ubuntu
WORKDIR /app
COPY requirements.txt requirements.txt
COPY light_tray_classifier.py ./
COPY jan28_Model.pth .

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 1883

RUN apt-get update -y
RUN apt-get install -y python3-pip android-tools-adb libssl-dev swig python3-dev gcc
RUN pip install -r requirements.txt
RUN mkdir images


CMD ["python3", "./light_tray_classifier.py"]