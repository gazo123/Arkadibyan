from fs_node import ForeignServer
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <fs_id>")
        return

    fs_id = int(sys.argv[1])
    fs = ForeignServer(fs_id)

    fs.register_and_receive()
    
    print(f"[FS {fs_id}] Running... waiting for PID.")
    fs.start_pid_listener()

    fs.start_share_request_listener()  # Keeps FS ready to respond

    if fs.check_if_user_present(fs.pid_dict):
        fs.broadcast_share_request(fs.user_id)


    while True:
        pass  # keep alive

if __name__ == "__main__":
    main()
