#!/bin/bash

service ssh start
service nginx start
chown -R debian-tor:debian-tor /var/lib/tor
chmod 700 /var/lib/tor
chmod 700 /var/lib/tor/hidden_service
su -s /bin/bash debian-tor -c "tor"