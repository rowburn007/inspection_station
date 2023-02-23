FROM ubuntu AS builder
WORKDIR /app
COPY requirements.txt requirements.txt
COPY light_tray_classifier.py ./
COPY jan28_Model.pth .

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip && \
    mkdir images && \
    pip install -r requirements.txt

FROM ubuntu
COPY --from=build ./app .
EXPOSE 1883
CMD ["python3", "./light_tray_classifier.py"]