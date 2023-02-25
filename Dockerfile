FROM ubuntu AS builder
WORKDIR /app
COPY requirements.txt .
COPY light_tray_classifier.py .
COPY jan28_Model.pth .

RUN apt-get update && \
    apt-get install -y python3-pip && \
    mkdir images && \
    pip install -r requirements.txt && \
    chmod +x light_tray_classifier.py


FROM alpine:latest
EXPOSE 1883
WORKDIR /app
COPY --from=builder /app /app
CMD [ "./light_tray_classifier.py" ]