import socket
import time

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024
NUM_PINGS = 10
TIMEOUT = 2.0
SLEEP_INTERVAL = 0.5


def create_udp_socket(timeout: float) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock


def send_ping(sock: socket.socket, host: str, port: int, index: int) -> bool:
    message = "PING"
    print(f"[Client] Ping #{index}: sending {message!r}...")
    sock.sendto(message.encode("utf-8"), (host, port))
    try:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        print(f"[Client] Ping #{index}: received {data.decode('utf-8')!r} ✓")
        return True
    except socket.timeout:
        print(f"[Client] Ping #{index}: TIMEOUT — reply lost (continuing...)")
        return False


def main():
    received = 0
    with create_udp_socket(TIMEOUT) as sock:
        print(f"[Client] Sending {NUM_PINGS} pings to {HOST}:{PORT}\n")
        for i in range(1, NUM_PINGS + 1):
            if send_ping(sock, HOST, PORT, i):
                received += 1
            time.sleep(SLEEP_INTERVAL)
    print(f"\n[Client] Done. Received {received}/{NUM_PINGS} replies.")


if __name__ == "__main__":
    main()
