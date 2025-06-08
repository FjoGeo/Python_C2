# C2 Server

A simple C2 server that controls an agent, allowing it to execute shell commands, capture keyboard input and upload and download files.

## C2 Server

    - Available as CLI and as a WebUI
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

## Future Upgrades

    - Multi-Agent handling
    - additional tools for enumeration
