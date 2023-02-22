# First stage
FROM python:3.9 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt


# Second stage
FROM python:3.9-slim
WORKDIR /app


COPY --from=builder . .
COPY light_tray_classifier.py .
COPY jan28_Model.pth .

RUN mkdir images

EXPOSE 1883

CMD ["python3", "./main_tray_classifier.py"]

