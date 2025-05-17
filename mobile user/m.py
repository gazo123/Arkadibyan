import socket
import json
import hashlib
import secrets

FS_IP = "100.88.231.34"  # IP of the Foreign Server
FS_PID_PORT = 9101       # Port FS is listening on

def generate_nonce(length=8):
    return secrets.token_hex(length)

def compute_pid(secret_key, user_id, nonce):
    combined = f"{secret_key}{user_id}{nonce}".encode()
    return hashlib.sha256(combined).hexdigest()

def send_pid(user_id, key):
    nonce = generate_nonce()
    pid = compute_pid(key, user_id, nonce)
    message = json.dumps({user_id: pid})

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((FS_IP, FS_PID_PORT))
            s.sendall(message.encode())
            print(f"[MobileUser] ✅ Sent PID: {pid}")
            print(f"[MobileUser] Used nonce: {nonce}")
    except Exception as e:
        print(f"[MobileUser] ❌ Failed to send PID: {e}")

if __name__ == "__main__":
    uid = input("Enter User ID: ").strip()
    key = input("Enter secret key: ").strip()  # Example: aa1b2c3d...
    send_pid(uid, key)
