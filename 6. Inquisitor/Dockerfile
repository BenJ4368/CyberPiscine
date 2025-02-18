FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip && \
    pip install scapy pyftpdlib && \
    mkdir ftp_serv_send ftp_serv_recv

COPY inquisitor.py .
COPY ftp_client.py .

EXPOSE 21

CMD ["/bin/bash"]

# python3 -m pyftpdlib -p 21 -w