# C2 Server

## C2 Server

    - Listens for connections from agents (via TCP or HTTP)
    - Receives agent info, sends commands
    - Stores logs (keystrokes, results, etc.)
    - Handles file transfers
    - Exposes a web dashboard (via Flask or FastAPI)

## Agent

    - Initiates connection (reverse shell model)
    - Listens for commands
    - Executes shell commands
    - Captures keystrokes (on host OS)
    - Handles file upload/download to/from server

## Project Structure

```
c2_project/
├── server/
│ ├── c2_server.py # TCP/HTTP server core
│ ├── dashboard.py # Flask dashboard
│ ├── agent_handler.py # Manage agent sessions
│ └── logs/ # Keystrokes, outputs
│
├── agent/
│ └── agent.py # Connects to C2
│
├── shared/
│ └── file_utils.py # Upload/download logic
```
