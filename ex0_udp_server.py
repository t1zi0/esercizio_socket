import socket

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024


def create_udp_socket(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[Server] Listening for UDP datagrams on {host}:{port} ...")
    return sock


def handle_message(message: str) -> str:
    if message == "PING":
        return "PONG"
    return f"Unknown: {message!r}"


def receive_and_reply(sock: socket.socket) -> None:
    data, client_addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8").strip()
    print(f"[Server] Received {message!r} from {client_addr}")
    reply = handle_message(message)
    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Sent {reply!r} to {client_addr}")


def main():
    with create_udp_socket(HOST, PORT) as sock:
        print("[Server] Press Ctrl+C to stop.\n")
        while True:
            receive_and_reply(sock)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Server] Stopped.")
