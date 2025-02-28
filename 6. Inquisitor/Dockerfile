FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpcap-dev && \
    pip install scapy

COPY inquisitor.py .

CMD ["sleep", "infinity"]