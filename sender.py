import os
import socket
import time

server = "192.168.1.2"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("waiting receiver...")
while True:
    try:
        s.connect((server, port))
        print("connected!")
        break
    except socket.error: # try again if some error
        time.sleep(2)

sender = os.path.join(os.environ['userprofile'], 'desktop', 'sender')

for root, dirs, files in os.walk(sender):
    for i in files:
        file_dir = os.path.join(root, i)
        
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