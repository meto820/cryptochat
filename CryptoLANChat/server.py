import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000

clients = {}  # username -> conn
lock = threading.Lock()

def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

users = load_users()

def broadcast(message, sender=None):
    with lock:
        for uname, conn in clients.items():
            if conn is not sender:
                try:
                    conn.sendall(message.encode("utf-8"))
                except:
                    pass

def send_dm(target, message):
    with lock:
        if target in clients:
            try:
                clients[target].sendall(message.encode("utf-8"))
            except:
                pass

def handle_client(conn, addr):
    conn.sendall("[server] LOGIN username:password veya REGISTER username:password\n".encode("utf-8"))
    try:
        data = conn.recv(1024).decode("utf-8").strip()
        if data.startswith("LOGIN"):
            _, creds = data.split(" ", 1)
            username, password = creds.split(":", 1)
            if username in users and users[username] == password:
                conn.sendall(f"[server] Hoş geldiniz {username}!\n".encode("utf-8"))
                with lock:
                    clients[username] = conn
                broadcast(f"[server] {username} bağlandı.\n", sender=conn)
            else:
                conn.sendall("[server] Kullanıcı adı veya şifre yanlış!\n".encode("utf-8"))
                conn.close()
                return
        elif data.startswith("REGISTER"):
            _, creds = data.split(" ", 1)
            username, password = creds.split(":", 1)
            if username in users:
                conn.sendall("[server] Bu kullanıcı zaten kayıtlı!\n".encode("utf-8"))
                conn.close()
                return
            users[username] = password
            save_users(users)
            conn.sendall(f"[server] Kayıt başarılı, hoş geldiniz {username}!\n".encode("utf-8"))
            with lock:
                clients[username] = conn
            broadcast(f"[server] {username} bağlandı.\n", sender=conn)
        else:
            conn.sendall("[server] Hatalı komut!\n".encode("utf-8"))
            conn.close()
            return

        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            text = msg.decode("utf-8").strip()
            if text.startswith("DM "):
                # Format: DM hedef_username: mesaj
                _, rest = text.split(" ", 1)
                if ":" in rest:
                    target, dm_msg = rest.split(":", 1)
                    send_dm(target.strip(), f"[DM] {dm_msg.strip()}")
            else:
                broadcast(text, sender=conn)

    except Exception as e:
        print(f"[server] Hata: {e}")
    finally:
        with lock:
            for uname, c in list(clients.items()):
                if c is conn:
                    del clients[uname]
                    broadcast(f"[server] {uname} ayrıldı.\n")
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[server] {HOST}:{PORT} üzerinde dinleniyor...")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()