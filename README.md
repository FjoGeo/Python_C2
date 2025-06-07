# C2 Server

A simple C2 server that controls an agent, allowing it to execute shell commands, capture keyboard input and upload and download files.

## C2 Server

    - Listens for connections from agents (via TCP or HTTP)
    - Receives agent info, sends commands
    - Stores logs (keystrokes, results, etc.)
    - Handles file transfers

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
│ └── logs/ # Keystrokes, outputs
│
├── agent/
│ └── agent.py # Connects to C2

```

## Future Upgrades

    - Dashboard with Flaks or Django
    - Multi-Agent handling
    - additional tools for enumeration
