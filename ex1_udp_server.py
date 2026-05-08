import socket

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024


def create_udp_socket(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[Server] Listening on {host}:{port} ... (Ctrl+C to stop)\n")
    return sock


def build_reply(message: str, count: int) -> str:
    if message == "PING":
        return f"PONG #{count}"
    return f"Unknown: {message!r}"


def main():
    ping_count = 0

    with create_udp_socket(HOST, PORT) as sock:
        while True:
            data, client_addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8").strip()

            if message == "PING":
                ping_count += 1

            reply = build_reply(message, ping_count)
            sock.sendto(reply.encode("utf-8"), client_addr)
            print(f"[Server] {client_addr} → {message!r}  |  replied: {reply!r}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Server] Stopped.")
