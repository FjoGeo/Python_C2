# Python_C2

## Architecture Overview

### C2 Server (Python)

    - Listens for connections from agents (via TCP or HTTP)
    - Receives agent info, sends commands
    - Stores logs (keystrokes, results, etc.)
    - Handles file transfers
    - Exposes a web dashboard (via Flask or FastAPI)
