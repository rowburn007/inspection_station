FROM python:3.9-slim AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
COPY jan28_Model.pth .
COPY light_tray_classifier.py .
RUN chmod 755 light_tray_classifier.py

FROM jeanblanchard/alpine-glibc
WORKDIR /tc
COPY --from=builder /app .
RUN apk add --update --no-cache && \
    apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

EXPOSE 1883
CMD [ "./light_tray_classifier.py" ]