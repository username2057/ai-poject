"""Start the FastAPI backend and Streamlit frontend in separate processes."""
import subprocess, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
backend=subprocess.Popen([sys.executable,"-m","uvicorn","app.backend.api:api","--host","127.0.0.1","--port","8000"],cwd=root)
try:
    subprocess.run([sys.executable,"-m","streamlit","run","app/main.py","--server.address","127.0.0.1"],cwd=root,check=True)
finally:
    backend.terminate(); backend.wait(timeout=10)
