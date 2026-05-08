import socket
import time

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
NUM_PINGS = 5
SLEEP_INTERVAL = 0.5


def create_client_socket(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"[Client] Connected to {host}:{port}")
    return sock


def send_ping(sock: socket.socket, index: int) -> str:
    message = "PING"
    print(f"\n[Client] Send #{index}: {message!r}")
    sock.sendall(message.encode("utf-8"))
    data = sock.recv(BUFFER_SIZE)
    return data.decode("utf-8")


def main():
    with create_client_socket(HOST, PORT) as sock:
        for i in range(1, NUM_PINGS + 1):
            reply = send_ping(sock, i)
            print(f"[Client] Reply: {reply!r}")
            time.sleep(SLEEP_INTERVAL)
    print("\n[Client] All pings sent. Connection closed.")


if __name__ == "__main__":
    main()
