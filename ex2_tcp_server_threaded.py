import socket
import threading

HOST = "127.0.0.1"
PORT = 65432
BACKLOG = 10
BUFFER_SIZE = 1024


def handle_message(message: str) -> str:
    if message == "PING":
        return "PONG"
    return f"Unknown: {message!r}"


def serve_client(conn: socket.socket, addr: tuple) -> None:
    tname = threading.current_thread().name
    print(f"[Server] [{tname}] Connected: {addr}")
    with conn:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print(f"[Server] [{tname}] {addr} disconnected.")
                break
            message = data.decode("utf-8").strip()
            reply = handle_message(message)
            conn.sendall(reply.encode("utf-8"))
            print(f"[Server] [{tname}] {addr}: {message!r} → {reply!r}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(BACKLOG)
        print(f"[Server] Threaded server on {HOST}:{PORT} — Ctrl+C to stop\n")

        while True:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=serve_client, args=(conn, addr), daemon=True)
            t.start()
            print(f"[Server] Spawned {t.name} for {addr} — active threads: {threading.active_count()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Server] Stopped.")
