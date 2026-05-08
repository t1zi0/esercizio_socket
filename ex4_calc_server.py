import socket

HOST = "127.0.0.1"
PORT = 65434
BACKLOG = 5
BUFFER_SIZE = 4096
SAFE_NAMESPACE = {"__builtins__": {}}


def create_server_socket(host: str, port: int, backlog: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(backlog)
    print(f"[Calc Server] Ready on {host}:{port}\n")
    return sock


def evaluate_expression(expr: str) -> str:
    try:
        result = eval(expr, SAFE_NAMESPACE)
        return f"RESULT: {result}"
    except ZeroDivisionError:
        return "ERROR: Division by zero"
    except Exception as e:
        return f"ERROR: {e}"


def serve_client(conn: socket.socket, addr: tuple) -> None:
    print(f"[Calc Server] Client connected: {addr}")
    with conn:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print(f"[Calc Server] {addr} disconnected abruptly.")
                break

            message = data.decode("utf-8").strip()
            print(f"[Calc Server] {addr} → {message!r}")

            if message.upper() == "QUIT":
                conn.sendall("BYE".encode("utf-8"))
                print(f"[Calc Server] {addr} requested QUIT. Closing.\n")
                break

            reply = evaluate_expression(message)
            conn.sendall(reply.encode("utf-8"))
            print(f"[Calc Server] → {reply!r}")


def main():
    with create_server_socket(HOST, PORT, BACKLOG) as server_sock:
        while True:
            conn, addr = server_sock.accept()
            serve_client(conn, addr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Calc Server] Stopped.")
