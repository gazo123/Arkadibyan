import socket
import json
from config import LISTEN_PORT, TOTAL_FOREIGN_SERVERS
from user_db import register_user, load_users
from share_manager import split_secret

def main():
    print("🏠 Home Server started...")
    
    # Step 1: Register users
    register_user("pushan123")
    register_user("arkapriya69")
    register_user("pritam420")

    users = load_users()

    # Step 2: Generate Shamir shares per FS
    shares_map = {1: {}, 2: {}, 3: {}}
    for uid, key in users.items():
        shares = split_secret(key)
        for i in range(3):
            shares_map[i+1][uid] = shares[i]

    # Step 3: Listen for FS connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", LISTEN_PORT))  # Accept connections from any machine
        s.listen()
        print(f"🔌 Listening on port {LISTEN_PORT}...")

        received = 0
        while received < TOTAL_FOREIGN_SERVERS:
            conn, addr = s.accept()
            with conn:
                print(f"🔔 Connection from {addr[0]}")
                try:
                    fs_id = int(conn.recv(1024).decode().strip())
                    if fs_id in shares_map:
                        data = json.dumps(shares_map[fs_id]).encode()
                        conn.sendall(data)
                        print(f"✅ Sent share to FS {fs_id}")
                        received += 1
                    else:
                        conn.sendall(b"Invalid FS ID")
                        print(f"⚠️ Unknown FS ID received: {fs_id}")
                except Exception as e:
                    print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
