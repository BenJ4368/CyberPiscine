import os
import time
from ftplib import FTP

ftp_host = "172.17.0.2"
ftp_port = 21
ftp_user = "anonymous"
ftp_pass = ""

source_dir = "/ftp_serv_send"
dest_dir = "/ftp_serv_recv"


def ftp_upload_file(ftp, file_path):
    try:
        ftp.cwd(dest_dir)
    except Exception as e:
        print(f"Error changing directory to {dest_dir}: {e}")
        return

    try:
        with open(file_path, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
            print(f"File {filename} uploaded successfully")
    except Exception as e:
        print(f"Error uploading file {filename}: {e}")

if __name__ == "__main__":
    ftp = FTP()
    try:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            print(f"Connected to FTP server {ftp_host}")
    except Exception as e:
            print(f"Error connecting to FTP server: {e}")
            exit()

    counter = 1
    while True:
        filename= f"FTP_TEST_{counter}.txt"
        file_content= f"FTP TEST {counter}: lorem ipsum dolor sit amet"

        file_path = os.path.join(source_dir, filename)
        os.makedirs(source_dir, exist_ok=True)
        with open(file_path, "w") as file:
            file.write(file_content)
        print(f"File {file_path} created")

        try:
            ftp_upload_file(ftp, file_path)
        except Exception as e:
            print(f"Error uploading file {filename}: {e}")
        
        time.sleep(10)
        counter += 1
