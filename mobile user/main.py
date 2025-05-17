from pid_utils import compute_pid, generate_nonce
from sender import send_pid_to_fs

def main():
    print("📱 Mobile User Login")

    user_id = input("Enter your User ID: ").strip()
    secret_key = input("Enter your secret key (K): ").strip()
    nonce = generate_nonce()

    pid = compute_pid(secret_key, user_id, nonce)
    print(f"[MobileUser] Computed PID: {pid}")
    print(f"[MobileUser] Using nonce: {nonce}")

    fs_id = int(input("Enter FS ID to send PID to (1-3): "))
    send_pid_to_fs(fs_id, user_id, pid)

if __name__ == "__main__":
    main()
