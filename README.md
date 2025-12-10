 Safe Code Executor (Python + Docker Sandbox)

A secure sandbox system that executes untrusted Python code inside a restricted Docker container.  
Designed for learning container security, resource isolation, and secure API design.

---

 Features

 Secure Python Code Execution
User-submitted Python runs safely inside a Docker container using:
- Timeout control
- Memory limits
- No filesystem write access
- No network connectivity
- Limited process count
- Dropped Linux capabilities

 REST API (Flask)
Endpoint:
POST /run
{
"code": "print(2+2)"
}


Response:


{
"status": "ok",
"output": "4\n",
"error": ""
}

 Web UI
A simple HTML client for running code directly from browser.


 Security Measures

| Risk | Mitigation | Implementation |
|------|------------|----------------|
| Infinite loops | Force-stop after 10 sec | `timeout=10` |
| Memory bombs | Limit container memory | `--memory=128m` |
| Fork bombs | Limit processes | `--pids-limit=64` |
| Network attacks | Disable networking | `--network=none` |
| Filesystem writes | Read-only filesystem | `--read-only` |
| Privilege escalation | Drop capabilities | `--cap-drop=ALL` |
| Container breakout | No mounts / isolated fs | No `-v` used |

This closely resembles how REPL, LeetCode, and Judge0 sandboxes work.


 Project Structure
safe-code-executor/
│
├── app.py # Flask API server
├── index.html # Web UI
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # Documentation

 Setup Instructions

 1. Create virtual environment

python3 -m venv venv
source venv/bin/activate


 2. Install dependencies


pip install -r requirements.txt


 3. Run the server


python app.py


Server runs on:


http://127.0.0.1:5000


 Security Test Cases

 Timeout test


while True:
pass

 `status: timeout`

 Memory limit test


x = "a" * 1000000000

 `status: runtime_error`

 Network disabled test


import socket
socket.gethostbyname("google.com")

 DNS failure

 Read-only filesystem test


open("/tmp/test.txt", "w").write("hello")

 `Read-only file system`

 Filesystem isolation test


open("/etc/passwd").read()

 Shows *container’s* file, NOT host’s

 What I Learned

- How Docker isolates processes, memory, and filesystem.
- Why executing untrusted code is dangerous.
- How resource limits prevent DoS attacks.
- Difference between container and host filesystem.
- Importance of dropping Linux capabilities.
- Real-world sandboxing techniques used by online judge systems.

 Possible Improvements

- Add support for Node.js, Java, C++
- Add multi-file upload (.zip)
- Add syntax highlighting (CodeMirror)
- Add rate limiting / user accounts
- Add database for execution logs
- Use gVisor / Firecracker for stronger security
- Deploy with Docker Compose
