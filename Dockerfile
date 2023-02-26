FROM python:3.9-slim AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
COPY jan28_Model.pth .
COPY light_tray_classifier.py .
RUN chmod 755 light_tray_classifier.py && \
    pip install --no-cache -r requirements.txt

EXPOSE 1883
CMD [ "./light_tray_classifier.py" ]