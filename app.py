from flask import Flask, request, jsonify
import subprocess
import shutil

app = Flask(__name__)

MAX_CODE_LENGTH = 5000
EXEC_TIMEOUT = 10
MAX_OUTPUT_CHARS = 10000
DOCKER_IMAGE = "python:3.11-slim"

# Check Docker installed
if shutil.which("docker") is None:
    raise RuntimeError("Docker not found. Install Docker first.")

DOCKER_CMD = [
    "docker", "run", "--rm", "-i",
    "--network", "none",
    "--memory", "128m",
    "--pids-limit", "64",
    "--read-only",
    "--cap-drop=ALL",
    "--security-opt", "no-new-privileges",
    DOCKER_IMAGE,
    "python", "-u", "-c",
    "import sys; code=sys.stdin.read(); exec(code, {})"
]

@app.route("/run", methods=["POST"])
def run_code():
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    if "code" not in data:
        return jsonify({"error": "Missing 'code'"}), 400

    code = data["code"]

    if not isinstance(code, str):
        return jsonify({"error": "Code must be a string"}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({"error": f"Code too long (max {MAX_CODE_LENGTH} chars)"}), 400

    code = code.replace("\x00", "")

    try:
        proc = subprocess.run(
            DOCKER_CMD,
            input=code,
            text=True,
            capture_output=True,
            timeout=EXEC_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "timeout",
            "output": "",
            "error": f"Execution timed out after {EXEC_TIMEOUT} seconds"
        }), 200

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    if proc.returncode != 0:
        if "MemoryError" in stderr:
            return jsonify({
                "status": "memory",
                "output": "",
                "error": "Memory limit reached"
            }), 200

        return jsonify({
            "status": "runtime_error",
            "output": stdout,
            "error": stderr
        }), 200

    return jsonify({
        "status": "ok",
        "output": stdout,
        "error": ""
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
