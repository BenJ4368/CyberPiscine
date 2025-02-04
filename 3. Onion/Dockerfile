FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /var/www/html/index.html

COPY torrc /etc/tor/torrc

RUN mkdir /var/run/sshd && \
    echo 'root:Test123!' | chpasswd && \
    sed -i 's/#\?PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#\?UsePAM .*/UsePAM no/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 4242/' /etc/ssh/sshd_config

RUN mkdir -p /var/lib/tor/hidden_service

EXPOSE 80
EXPOSE 4242

COPY script.sh /script.sh
RUN chmod +x /script.sh

CMD ["/script.sh"]