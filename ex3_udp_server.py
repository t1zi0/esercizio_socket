import socket
import random

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024
DROP_PROBABILITY = 0.3


def create_udp_socket(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[Server] Listening on {host}:{port} (drop prob={DROP_PROBABILITY:.0%})\n")
    return sock


def should_drop() -> bool:
    return random.random() < DROP_PROBABILITY


def build_reply(message: str) -> str:
    if message == "PING":
        return "PONG"
    return f"Unknown: {message!r}"


def main():
    with create_udp_socket(HOST, PORT) as sock:
        while True:
            data, client_addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8").strip()
            print(f"[Server] Received {message!r} from {client_addr}")

            reply = build_reply(message)

            if should_drop():
                print("[Server] *** Dropped reply (simulated packet loss) ***\n")
                continue

            sock.sendto(reply.encode("utf-8"), client_addr)
            print(f"[Server] Sent {reply!r} to {client_addr}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Server] Stopped.")
