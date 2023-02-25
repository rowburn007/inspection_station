FROM ubuntu AS builder
WORKDIR /app
COPY requirements.txt .
COPY light_tray_classifier.py .
COPY jan28_Model.pth .
RUN apt-get update && \
    apt-get install -y python3-pip && \
    mkdir images && \
    pip install -r requirements.txt && \
    chmod 755 light_tray_classifier.py


FROM ubuntu
COPY --from=builder / /
EXPOSE 1883
CMD [ "./app/light_tray_classifier.py" ]