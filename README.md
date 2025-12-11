Safe Python Executor

A secure Python execution environment built using Flask, AST-based sandboxing, and Docker container isolation.
This project ensures that untrusted Python code executes safely, with strict restrictions and strong security boundaries.

 Features
1. AST-Level Code Sandboxing

Before execution, your server parses user code using Python’s ast module and blocks dangerous operations such as:

import statements

open, exec, eval, compile

os, sys, socket, shutil, ctypes

Attribute access like os.system, sys.modules

This prevents harmful code even before Docker executes it.

2. Docker Container Isolation

Every execution runs inside a temporary Docker container:

Protection	Value
Filesystem	Read-only
Memory	128MB
CPU	0.5
PIDs	64
Network	Disabled
Storage	Tmpfs /tmp only

If the container hangs, it is automatically killed.

3. Output Modes

Your API supports two response formats:

 JSON Mode (Default)
{
  "exit_code": 0,
  "stdout": "Hello World\n",
  "stderr": ""
}

 Raw Mode (/run?raw=1)

Outputs plain text:

Hello World

4. Web User Interface

A clean HTML + CSS UI is included:

Code editor textarea

Run button

Dark-themed output console

Works seamlessly with the API

5. Full Error Handling

Syntax validation

Timeout handling

Docker runtime errors

Rejected unsafe code

Truncated large outputs

 Project Structure
safe-executor/
│── app.py              # Flask backend
│── requirements.txt    # Dependencies
│── templates/
│     └── index.html    # Web interface
│── .venv/              # Virtual environment

 Installation & Setup
1️ Clone the project
git clone <your_repo_url>
cd safe-executor

2️ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

3️ Install dependencies
pip install -r requirements.txt

4️ Run the server
python app.py


Server available at:

 http://127.0.0.1:5000

 API Usage
JSON Mode
curl -X POST "127.0.0.1:5000/run" \
-H "Content-Type: application/json" \
-d '{"code":"print(\"Hello World\")"}'

Raw Output Mode
curl -X POST "127.0.0.1:5000/run?raw=1" \
-H "Content-Type: application/json" \
-d '{"code":"print(\"Hello World\")"}'

 Security Measures
 AST sandbox blocks:

Imports

Dangerous built-ins

Dangerous modules

File access

Network access

Attribute chains

 Docker provides:

Full OS-level isolation

No persistent storage

No external networking

Low memory / CPU limits

 Server enforces:

Max code length

Max output length

Timeout kill

Clean error responses


 What I Learned

How sandboxing works using Python AST

How Docker isolates untrusted code

How to design secure execution pipelines

Flask API design with JSON & Raw modes

Building a clean UI for code execution

Real-world error handling and resource limits

 Final Statement

This project shows a complete secure execution pipeline using:

➡ AST security
➡ Docker containerization
➡ Flask backend
➡ Web UI

It is reliable, safe, and demonstrates strong understanding of secure system design.
