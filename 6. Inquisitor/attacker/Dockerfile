FROM debian:stable-slim

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y \
    tcpdump \
    iproute2 \
    iputils-ping \
    python3 \
    python3-scapy \
    iputils-arping

COPY inquisitor.py .

CMD ["bash"]