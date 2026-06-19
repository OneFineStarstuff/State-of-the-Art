FROM python:3.11-slim

WORKDIR /app

# Create a non-privileged user
RUN useradd -m sentinel && \
    mkdir -p /var/log/sentinel && \
    chown sentinel:sentinel /var/log/sentinel

COPY omni_sentinel_24h_monitor.py .

USER sentinel

ENV PYTHONUNBUFFERED=1
ENV LOG_PATH=/var/log/sentinel

CMD ["python", "omni_sentinel_24h_monitor.py"]
