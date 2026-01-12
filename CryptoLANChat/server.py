import socket
import threading
import json

HOST = "0.0.0.0"   # Tüm IP’lerden bağlantı kabul et
PORT = 5000

clients = []
lock = threading.Lock()

# Kullanıcı verilerini yükle
def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Kullanıcı verilerini kaydet
def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

users = load_users()

def broadcast(message, sender=None):
    with lock:
        for client in clients:
            if client is not sender:
                try:
                    client.sendall(message.encode("utf-8"))
                except:
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[+] Yeni bağlantı: {addr}")
    conn.sendall("[server] Giriş için: LOGIN username:password\n".encode("utf-8"))
    conn.sendall("[server] Kayıt için: REGISTER username:password\n".encode("utf-8"))

    try:
        data = conn.recv(1024).decode("utf-8").strip()
        if not data:
            conn.close()
            return

        if data.startswith("LOGIN"):
            _, creds = data.split(" ", 1)
            username, password = creds.split(":", 1)

            if username in users and users[username] == password:
                conn.sendall(f"[server] Hoş geldiniz {username}!\n".encode("utf-8"))
                with lock:
                    clients.append(conn)
                broadcast(f"[server] {username} bağlandı.\n", sender=conn)

                while True:
                    msg = conn.recv(1024)
                    if not msg:
                        break
                    text = msg.decode("utf-8").strip()
                    if text.lower() == "/quit":
                        break
                    broadcast(f"{username}: {text}\n", sender=conn)
            else:
                conn.sendall("[server] Kullanıcı adı veya şifre yanlış!\n".encode("utf-8"))
                conn.close()

        elif data.startswith("REGISTER"):
            _, creds = data.split(" ", 1)
            username, password = creds.split(":", 1)

            if username in users:
                conn.sendall("[server] Bu kullanıcı zaten kayıtlı!\n".encode("utf-8"))
                conn.close()
            else:
                users[username] = password
                save_users(users)
                conn.sendall(f"[server] Kayıt başarılı, hoş geldiniz {username}!\n".encode("utf-8"))
                with lock:
                    clients.append(conn)
                broadcast(f"[server] {username} bağlandı.\n", sender=conn)

                while True:
                    msg = conn.recv(1024)
                    if not msg:
                        break
                    text = msg.decode("utf-8").strip()
                    if text.lower() == "/quit":
                        break
                    broadcast(f"{username}: {text}\n", sender=conn)
        else:
            conn.sendall("[server] Hatalı komut!\n".encode("utf-8"))
            conn.close()

    except Exception as e:
        print(f"[server] Hata: {e}")
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[-] Bağlantı kapandı: {addr}")

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