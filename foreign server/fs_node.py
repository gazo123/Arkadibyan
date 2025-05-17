import socket
import os
from config import HOME_IP, HOME_PORT, SHARE_DIR, PID_PORT_OFFSET
import threading
import json

class ForeignServer:
    def __init__(self, fs_id):
        self.fs_id = fs_id
        self.user_pid = {}  # Stores {user_id: pid}
        self.share_file = os.path.join(SHARE_DIR, f"share_{fs_id}.json")
        os.makedirs(SHARE_DIR, exist_ok=True)

    def register_and_receive(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOME_IP, HOME_PORT))
                s.sendall(str(self.fs_id).encode())
                print(f"[FS {self.fs_id}] Connected to Home Server")

                data = s.recv(4096).decode()
                with open(self.share_path, "w") as f:
                    f.write(data)
                print(f"[FS {self.fs_id}] ✅ Share saved to {self.share_path}")

        except Exception as e:
            print(f"[FS {self.fs_id}] ❌ Error: {e}")


    def start_pid_listener(self):
        port = 9000 + self.fs_id + PID_PORT_OFFSET
        print(f"[FS {self.fs_id}] PID listener on port {port}")

        def listener():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('0.0.0.0', port))
                    s.listen()
                    print(f"[FS {self.fs_id}] Listening for PID on port {port}...")

                    while True:
                        conn, addr = s.accept()
                        with conn:
                            data = conn.recv(1024).decode()
                            try:
                                pid_data = json.loads(data)
                                self.user_pid.update(pid_data)
                                print(f"[FS {self.fs_id}] ✅ Received PID: {pid_data}")
                            except Exception as e:
                                print(f"[FS {self.fs_id}] ❌ JSON error: {e}")
            except Exception as e:
                print(f"[FS {self.fs_id}] ❌ PID Listener failed: {e}")

        threading.Thread(target=listener, daemon=True).start()
