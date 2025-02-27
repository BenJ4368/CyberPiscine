FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libcap-dev && \
    pip install scapy

COPY inquisitor.py .

CMD ["sleep", "infinity"]