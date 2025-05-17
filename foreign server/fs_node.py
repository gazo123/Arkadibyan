# import socket
# import os
# from config import HOME_IP, HOME_PORT, SHARE_DIR, PID_PORT_OFFSET
# import threading
# import json

# class ForeignServer:
#     def __init__(self, fs_id):
#         self.fs_id = fs_id
#         self.user_pid = {}  # Stores {user_id: pid}
#         self.share_path = os.path.join(SHARE_DIR, f"share_{fs_id}.json")
#         os.makedirs(SHARE_DIR, exist_ok=True)
            
#     def register_and_receive(self):
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.connect((HOME_IP, HOME_PORT))
#                 s.sendall(str(self.fs_id).encode())
#                 print(f"[FS {self.fs_id}] Connected to Home Server")

#                 data = s.recv(4096).decode()
#                 with open(self.share_path, "w") as f:
#                     f.write(data)
#                 print(f"[FS {self.fs_id}] ✅ Share saved to {self.share_path}")

#         except Exception as e:
#             print(f"[FS {self.fs_id}] ❌ Error: {e}")

                
#     def start_pid_listener(self):
#         port = 9000 + self.fs_id + PID_PORT_OFFSET
#         print(f"[FS {self.fs_id}] PID listener on port {port}")

#         def listener():
#             try:
#                 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#                     s.bind(("0.0.0.0", port))  # FS machine IP

#                     s.listen()
#                     print(f"[FS {self.fs_id}] Listening for PID on port {port}...")

#                     while True:
#                         conn, addr = s.accept()
#                         with conn:
#                             data = conn.recv(4096).decode()
#                             try:
#                                 pid_data = json.loads(data)
#                                 self.user_pid.update(pid_data)
#                                 print(f"[FS {self.fs_id}] ✅ Received PID: {pid_data}")
#                                 self.check_if_user_present(pid_data)
                                
#                             except Exception as e:
#                                 print(f"[FS {self.fs_id}] ❌ JSON error: {e}")
#             except Exception as e:
#                 print(f"[FS {self.fs_id}] ❌ PID Listener failed: {e}")

#         threading.Thread(target=listener, daemon=True).start()

        
import socket
import os
import threading
import json
from config import HOME_IP, HOME_PORT, SHARE_DIR, PID_PORT_OFFSET, FOREIGN_SERVERS, SHARE_REQUEST_PORT_OFFSET


class ForeignServer:
    def __init__(self, fs_id):
        self.fs_id = fs_id
        self.user_pid = {}  # Stores {user_id: pid}
        self.share_path = os.path.join(SHARE_DIR, f"share_{fs_id}.json")
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
                    s.bind(("0.0.0.0", port))  # FS machine IP

                    s.listen()
                    print(f"[FS {self.fs_id}] Listening for PID on port {port}...")

                    while True:
                        conn, addr = s.accept()
                        with conn:
                            data = conn.recv(4096).decode()
                            try:
                                pid_data = json.loads(data)
                                self.user_pid.update(pid_data)
                                print(f"[FS {self.fs_id}] ✅ Received PID: {pid_data}")
                                
                            except Exception as e:
                                print(f"[FS {self.fs_id}] ❌ JSON error: {e}")
            except Exception as e:
                print(f"[FS {self.fs_id}] ❌ PID Listener failed: {e}")

        threading.Thread(target=listener, daemon=True).start()

    def check_if_user_present(self, user_pid_dict):
        """
        Checks if the user_id from the given PID dict is present in the local share file.
        """
        if not os.path.exists(self.share_path):
            print(f"[FS {self.fs_id}] ❌ Share file does not exist: {self.share_path}")
            return

        try:
            with open(self.share_path, 'r') as f:
                share_data = json.load(f)
            user_id = next(iter(user_pid_dict))  # Extract first key
            if user_id in share_data:
                print(f"[FS {self.fs_id}] ✅ User '{user_id}' is present in share file.")
            else:
                print(f"[FS {self.fs_id}] ❌ User '{user_id}' NOT found in share file.")
        except Exception as e:
            print(f"[FS {self.fs_id}] ❌ Error reading share file: {e}")

    
    def broadcast_share_request(self, user_id):
        
        print(f"[FS {self.fs_id}] 📡 Broadcasting share request for '{user_id}' to peers...")
        for peer_id, (peer_ip, base_port) in FOREIGN_SERVERS.items():
            if peer_id == self.fs_id:
                continue  # Skip self
            try:
                target_port = base_port + SHARE_REQUEST_PORT_OFFSET
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((peer_ip, target_port))
                    s.sendall(user_id.encode())
                    print(f"[FS {self.fs_id}] ➡️ Sent share request to FS {peer_id} at {peer_ip}:{target_port}")
            except Exception as e:
                print(f"[FS {self.fs_id}] ❌ Failed to reach FS {peer_id}: {e}")

    def get_share_for_user(self, user_id):
        """
        Retrieves this FS's share for a specific user.
        """
        if not os.path.exists(self.share_path):
            return None
        try:
            with open(self.share_path, 'r') as f:
                share_data = json.load(f)
            return share_data.get(user_id)
        except:
            return None


    def start_share_request_listener(self):
        """
        Listens for incoming share requests from other FSs and sends back the share for the requested user_id.
        """
        port = 9000 + self.fs_id + SHARE_REQUEST_PORT_OFFSET
        print(f"[FS {self.fs_id}] 🛡 Listening for share requests on port {port}...")

        def handler():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', port))
                s.listen()

                while True:
                    conn, addr = s.accept()
                    with conn:
                        try:
                            user_id = conn.recv(1024).decode().strip()
                            share = self.get_share_for_user(user_id)
                            if share:
                                conn.sendall(json.dumps(share).encode())
                                print(f"[FS {self.fs_id}] 📤 Sent share for '{user_id}' to {addr[0]}")
                            else:
                                conn.sendall(b'{}')  # Empty response if not found
                        except Exception as e:
                            print(f"[FS {self.fs_id}] ❌ Error handling request: {e}")
        threading.Thread(target=handler, daemon=True).start()
