# C2 Server

A simple C2 (Command and Control) server that controls an agent, allowing it to execute shell commands, capture keyboard input, and upload/download files.

## Features

### C2 Server

- Available as a **CLI** and as a **WebUI**
- Listens for connections from agents (via TCP)
- Sends commands and receives output from agents
- Stores logs (keystrokes, command results, etc.)
- Handles file transfers (upload/download)

### Agent

- Initiates connection to the server (reverse shell model)
- Executes remote shell commands
- Captures keystrokes (basic keylogger)
- Uploads and downloads files

---

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/FjoGeo/Python_C2.git
   cd Python_C2

   ```

2. **Install dependencies**

   ```bash
   pip install flask pynput
   ```

---

## 🚀 Usage

### 🖥️ Start the C2 Server (CLI)

```bash
 python server/c2_server.py
```

### 🌐 Start the WebUI (Flask)

```bash
   python server/c2_webui.py
```

Then open a browser and go to:

    - http://127.0.0.1:5000 (on the same machine)
    - or http://<your-local-ip>:5000 (from another device on your network)

From there you can:

    - Enter and send commands
    - View output from the agent
    - Upload and download files

### 🕵️‍♂️ Start the Agent

Edit the IP address in agent.py to match your server:

```bash
server_host = "192.168.x.x"
server_port = 9999
```

Then run the agent on the target machine:

```bash
python agent.py
```
