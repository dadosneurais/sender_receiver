import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 4444))
s.listen(1)

print("waiting...")

conn, address = s.accept()
stream = conn.makefile('rb')

while True:

    try:

        line_name = stream.readline()

        if not line_name:
            break

        file_name = line_name.decode(errors="ignore").strip()

        print(f"Receiving: {file_name}")

        with open(file_name, "wb") as f:

            while True:

                data = stream.readline()

                if b"---end---" in data or not data:
                    break

                f.write(data)

        print("done:", file_name)

    except Exception as e:

        print("erro:", e)
        continue

conn.close()
s.close()

print("done!")
