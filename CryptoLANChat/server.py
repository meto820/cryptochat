import socket
import threading

HOST = "0.0.0.0"   # Tüm ağ arayüzlerinden bağlantı kabul eder
PORT = 5000        # İstediğin portu seçebilirsin

clients = []       # Bağlı client listesi
lock = threading.Lock()

def broadcast(message, sender=None):
    """Mesajı tüm clientlere gönderir"""
    with lock:
        for client in clients:
            if client is not sender:  # Gönderen hariç tutmak istersen
                try:
                    client.sendall(message.encode("utf-8"))
                except:
                    clients.remove(client)

def handle_client(conn, addr):
    """Her client için ayrı thread"""
    print(f"[+] Yeni bağlantı: {addr}")
    conn.sendall("[server] Hoş geldiniz!\n".encode("utf-8"))
    broadcast(f"[server] {addr} bağlandı.\n", sender=conn)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8").strip()
            if msg.lower() == "/quit":
                conn.sendall("[server] Çıkış yapılıyor...\n".encode("utf-8"))
                break
            print(f"[{addr}] {msg}")
            broadcast(f"[{addr}] {msg}\n", sender=conn)
        except:
            break

    with lock:
        if conn in clients:
            clients.remove(conn)
    conn.close()
    print(f"[-] Bağlantı kapandı: {addr}")
    broadcast(f"[server] {addr} ayrıldı.\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[server] {HOST}:{PORT} üzerinde dinleniyor...")

    while True:
        conn, addr = server_socket.accept()
        with lock:
            clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()