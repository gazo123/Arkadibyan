import sys
from fs_node import ForeignServer

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <fs_id>")
        return

    fs_id = int(sys.argv[1])
    fs = ForeignServer(fs_id)
    fs.register_and_receive()

    fs.start_pid_listener()

    print(f"[FS {fs_id}] ✅ Ready and waiting for PID messages...")

    # Keep the process alive
    while True:
        pass

if __name__ == "__main__":
    main()
