# from fs_node import ForeignServer
# import sys

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python main.py <fs_id>")
#         return

#     fs_id = int(sys.argv[1])
#     fs = ForeignServer(fs_id)

#     fs.register_and_receive()
    
#     print(f"[FS {fs_id}] Running... waiting for PID.")
#     fs.start_pid_listener()

#     fs.start_share_request_listener()  # Keeps FS ready to respond

    
#     if fs.check_if_user_present(fs.user_pid):
#         fs.broadcast_share_request(fs.user_id)

#     while True:
#         pass  # keep alive

# if __name__ == "__main__":
#     main()
from fs_node import ForeignServer
import sys
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <fs_id>")
        return

    fs_id = int(sys.argv[1])
    fs = ForeignServer(fs_id)

    fs.register_and_receive()
    fs.start_pid_listener()
    fs.start_share_request_listener()

    print(f"[FS {fs_id}] ✅ Running. Waiting for Mobile User PID...\n")

    try:
        while True:
            if fs.user_pid:
                user_id = list(fs.user_pid.keys())[0]  # Take first user received

                if fs.check_if_user_present(fs.user_pid):
                    print(f"\n[FS {fs_id}] ✅ UserID '{user_id}' is valid in local share.")

                    choice = input(f"[FS {fs_id}] ❓ Do you want to broadcast a share request for '{user_id}'? (y/n): ").strip().lower()
                    if choice == 'y':
                        fs.broadcast_share_request(user_id)

                    # Reset so it doesn't repeat
                    fs.user_pid.clear()
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n[FS {fs_id}] 🛑 Shutting down.")

if __name__ == "__main__":
    main()
