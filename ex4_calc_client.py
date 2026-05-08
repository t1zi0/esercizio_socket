import socket

HOST = "127.0.0.1"
PORT = 65434
BUFFER_SIZE = 4096


def create_client_socket(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"[Calc Client] Connected to {host}:{port}")
    print("[Calc Client] Type arithmetic expressions (e.g. '3 + 4', '2 ** 10').")
    print("[Calc Client] Type 'quit' to exit.\n")
    return sock


def run_session(sock: socket.socket) -> None:
    while True:
        try:
            expr = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            expr = "QUIT"

        if not expr:
            continue

        sock.sendall(expr.encode("utf-8"))
        data = sock.recv(BUFFER_SIZE)
        reply = data.decode("utf-8")
        print(f"    {reply}")

        if expr.upper() == "QUIT":
            break


def main():
    with create_client_socket(HOST, PORT) as sock:
        run_session(sock)
    print("[Calc Client] Session ended.")


if __name__ == "__main__":
    main()
