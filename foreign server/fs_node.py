import socket
import os
from config import HOME_IP, HOME_PORT, SHARE_DIR, PID_PORT_OFFSET
import threading
import json

class ForeignServer:
    def __init__(self, fs_id):
        self.fs_id = fs_id
        os.makedirs(SHARE_DIR, exist_ok=True)
        self.share_path = f"{SHARE_DIR}/share_{fs_id}.json"

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
        print(f"[FS {self.fs_id}] Listening for PID messages on port {port}...")

        def handler():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        try:
                            data = conn.recv(1024).decode()
                            pid_data = json.loads(data)
                            self.user_pid.update(pid_data)
                            print(f"[FS {self.fs_id}] ✅ Received PID: {pid_data}")
                        except Exception as e:
                            print(f"[FS {self.fs_id}] ❌ Failed to parse PID: {e}")

        threading.Thread(target=handler, daemon=True).start()