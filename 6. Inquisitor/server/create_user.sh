#!/bin/bash

SERVER_PASSWORD=serv_pass
SERVER_USERNAME=serv_user

echo "SERVER_USERNAME: $SERVER_USERNAME"
echo "SERVER_PASSWORD: $SERVER_PASSWORD"


useradd -m $SERVER_USERNAME
if [ $? -ne 0 ]; then
    echo "Failed to create user $SERVER_USERNAME. Please check the user name and try again."
    exit 1
fi

echo "$SERVER_USERNAME:$SERVER_PASSWORD" | chpasswd
if [ $? -ne 0 ]; then
    echo "Failed to set password for user $SERVER_USERNAME. Please check the password and try again."
    exit 1
fi

mkdir -p /home/$SERVER_USERNAME/ftp/upload
chown nobody:nogroup /home/$SERVER_USERNAME/ftp
chmod a-w /home/$SERVER_USERNAME/ftp
chown $SERVER_USERNAME:$SERVER_USERNAME /home/$SERVER_USERNAME/ftp/upload
if [ $? -ne 0 ]; then
    echo "Failed to set permissions for /home/$SERVER_USERNAME/ftp/upload. Please check the permissions and try again."
    exit 1
fi

echo "User $SERVER_USERNAME created successfully with home directory /home/$SERVER_USERNAME and password set."