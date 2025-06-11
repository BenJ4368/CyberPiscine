FROM debian:stable-slim

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y vsftpd openssl

RUN mkdir -p /var/run/vsftpd/empty

COPY create_user.sh .
COPY script.sh .
COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21

RUN chmod +x create_user.sh script.sh
RUN ./create_user.sh

ENTRYPOINT [ "./script.sh" ]
CMD ["bash"]