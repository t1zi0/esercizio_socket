import socket
import time

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024
NUM_PINGS = 5
TIMEOUT = 2.0
SLEEP_INTERVAL = 0.5


def create_udp_socket(timeout: float) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock


def send_ping(sock: socket.socket, host: str, port: int, index: int) -> None:
    message = "PING"
    print(f"[Client] Send #{index}: {message!r}")
    sock.sendto(message.encode("utf-8"), (host, port))
    try:
        data, server_addr = sock.recvfrom(BUFFER_SIZE)
        print(f"[Client] Reply from {server_addr}: {data.decode('utf-8')!r}")
    except socket.timeout:
        print(f"[Client] Timeout — no reply for ping #{index}")


def main():
    with create_udp_socket(TIMEOUT) as sock:
        print(f"[Client] Sending {NUM_PINGS} pings to {HOST}:{PORT}\n")
        for i in range(1, NUM_PINGS + 1):
            send_ping(sock, HOST, PORT, i)
            time.sleep(SLEEP_INTERVAL)
    print("\n[Client] Done.")


if __name__ == "__main__":
    main()
