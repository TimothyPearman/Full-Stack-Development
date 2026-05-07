# this file is just for me to run the the entire project with a single click becuase im lazy :D
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT_DIR = Path(__file__).resolve().parent                          # project root directory
PYTHON_EXECUTABLE = ROOT_DIR / ".venv" / "Scripts" / "python.exe"   # python executable path

FRONTEND_DIR = ROOT_DIR / "frontend"                                # frontend code directory    
FRONTEND_HEALTH_URL = "http://127.0.0.1:5500"                       # frontend root url
FRONTEND_OPEN_URL = "http://127.0.0.1:5500/index.html"              # frontend test url 
FRONTEND_COMMAND = [                                                # terminal command to start frontend server with python http.server module
    PYTHON_EXECUTABLE,
    "-m",
    "http.server", 
    "5500"
]
        
BACKEND_DIR = ROOT_DIR / "backend"                                  # backend code directory
BACKEND_HEALTH_URL = "http://127.0.0.1:8000"                        # backend root url
BACKEND_OPEN_URL = "http://127.0.0.1:8000/docs"                     # backend test url
BACKEND_COMMAND = [                                                 # terminal command to start backend server with uvicorn
    PYTHON_EXECUTABLE,                                              # python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
    "-m",
    "uvicorn",
    "main:app",
    "--reload",
    "--host",  
    "127.0.0.1",
    "--port",
    "8000"
]

def get_python_executable() -> str:
    """ returns path to Python executable in  virtual environment """
    python_executable = ROOT_DIR / ".venv" / "Scripts" / "python.exe"   # python executable path

    if python_executable.exists():                                      # ensure python executable exists
        return str(python_executable)                                   # return found python executable

    return sys.executable  

class Server:
        def __init__(self, name: str, start_command: list[str], process: subprocess.Popen | None, health_url: str, open_url: str, cwd: Path):
            self.name = name
            self.start_command = start_command

            self.process = process
            self.health_url = health_url
            self.open_url = open_url
            self.timeout = 0
            self.cwd = cwd
            
    
        def start(self):
            self.process = subprocess.Popen(self.start_command, cwd=str(self.cwd))    # terminal command to start server
    
        def open(self, timeout=20):
            if self.process is None:
                print(f"{self.name} process is not running")
                return
            
            deadline = time.time() + timeout
            while time.time() < deadline:
                if self.process.poll() is not None:
                    print(f"{self.name} process exited unexpectedly")
                    return
                
                try:
                    with urlopen(self.health_url, timeout=1):   # check if server is healthy
                        webbrowser.open(self.open_url)          # open in browser when healthy
                        return
                except URLError:
                    time.sleep(0.5)                             # wait before retrying

        def stop(self):
            if self.process is None:
                print(f"{self.name} process is not running")
                return
            
            if self.process.poll() is not None:
                return
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
if __name__ == "__main__":
    frontend = Server("Frontend", FRONTEND_COMMAND, None, FRONTEND_HEALTH_URL, FRONTEND_OPEN_URL, FRONTEND_DIR)
    backend = Server("Backend", BACKEND_COMMAND, None, BACKEND_HEALTH_URL, BACKEND_OPEN_URL, BACKEND_DIR)

    frontend.start()
    backend.start()

    frontend.open()
    backend.open()

    try:
        while True:
            if frontend.process is None or frontend.process.poll() is not None:
                raise RuntimeError("Frontend process exited")
            if backend.process is None or backend.process.poll() is not None:
                raise RuntimeError("Backend process exited")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        frontend.stop()
        backend.stop()