FROM ubuntu

WORKDIR /app


COPY main_tray_classifier.py .
COPY jan28_Model.pth .

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 3000
EXPOSE 1883

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install paho-mqtt
RUN apt-get install -y android-tools-adb
RUN mkdir images

CMD ["ubuntu", "-d", "daemon off"]

