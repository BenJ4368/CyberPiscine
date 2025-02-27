#!/bin/sh

apk add --no-cache lftp

while true; do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    FILE="/client/uploads/test_$TIMESTAMP.txt"
    
    echo "Fichier envoyé à $TIMESTAMP" > "$FILE"

    lftp -u "$FTP_USER_NAME","$FTP_USER_PASS" ftp-server -e "put $FILE; bye"

    echo "Fichier $FILE envoyé."
    sleep 60
done
