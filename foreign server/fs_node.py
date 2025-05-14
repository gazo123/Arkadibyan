import socket
import os
from config import HOME_IP, HOME_PORT, SHARE_DIR

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
