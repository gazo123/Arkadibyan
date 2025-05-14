import sys
from fs_node import ForeignServer

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <fs_id>")
        return

    fs_id = int(sys.argv[1])
    fs = ForeignServer(fs_id)
    fs.register_and_receive()

if __name__ == "__main__":
    main()
