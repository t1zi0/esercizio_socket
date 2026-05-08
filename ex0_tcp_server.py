import socket

HOST = "127.0.0.1"
PORT = 65432
BACKLOG = 1
BUFFER_SIZE = 1024


def create_server_socket(host: str, port: int, backlog: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(backlog)
    print(f"[Server] Listening on {host}:{port} ...")
    return sock


def handle_message(message: str) -> str:
    if message == "PING":
        return "PONG"
    return f"Unknown: {message!r}"


def serve_client(conn: socket.socket, addr: tuple) -> None:
    print(f"[Server] Connection accepted from {addr}")
    with conn:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print("[Server] Client closed the connection.")
                break
            message = data.decode("utf-8").strip()
            print(f"[Server] Received: {message!r}")
            reply = handle_message(message)
            conn.sendall(reply.encode("utf-8"))
            print(f"[Server] Sent: {reply!r}")


def main():
    with create_server_socket(HOST, PORT, BACKLOG) as server_sock:
        conn, addr = server_sock.accept()
        serve_client(conn, addr)


if __name__ == "__main__":
    main()
