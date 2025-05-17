import socket
import json
from config import FOREIGN_SERVERS, PID_PORT_OFFSET

def send_pid_to_fs(fs_id, user_id, pid):
    if fs_id not in FOREIGN_SERVERS:
        raise ValueError(f"Invalid FS ID: {fs_id}")

    ip, base_port = FOREIGN_SERVERS[fs_id]
    port = base_port + PID_PORT_OFFSET

    message = json.dumps({user_id: pid})

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(message.encode())
            print(f"[MobileUser] ✅ Sent PID to FS {fs_id} at {ip}:{port}")
    except Exception as e:
        print(f"[MobileUser] ❌ Failed to send PID: {e}")
