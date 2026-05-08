import socket

HOST = "127.0.0.1"
PORT = 65432
BACKLOG = 5
BUFFER_SIZE = 1024
MAX_CLIENTS = 3


def create_server_socket(host: str, port: int, backlog: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(backlog)
    print(f"[Server] Listening on {host}:{port} (max {MAX_CLIENTS} clients)")
    return sock


def handle_message(message: str) -> str:
    if message == "PING":
        return "PONG"
    return f"Unknown: {message!r}"


def serve_client(conn: socket.socket, addr: tuple) -> None:
    print(f"[Server] Connected: {addr}")
    with conn:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print(f"[Server] {addr} disconnected.")
                break
            message = data.decode("utf-8").strip()
            reply = handle_message(message)
            conn.sendall(reply.encode("utf-8"))
            print(f"[Server] {addr}: {message!r} → {reply!r}")


def main():
    with create_server_socket(HOST, PORT, BACKLOG) as server_sock:
        for client_num in range(1, MAX_CLIENTS + 1):
            print(f"\n[Server] Waiting for client #{client_num}...")
            conn, addr = server_sock.accept()
            serve_client(conn, addr)
    print("[Server] Reached max clients. Shutting down.")


if __name__ == "__main__":
    main()
