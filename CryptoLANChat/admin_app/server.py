import socket
import threading
import json
import sys

from PySide6.QtWidgets import QApplication

from admin_app.auth import check_admin_password
from admin_app.ui.admin_panel import AdminPanel

from share.crypto import encrypt, decrypt
from share.config import HOST, PORT, ROOM_KEY
from share.state import online_users


# ─────────────────────────────
# ADMIN PAROLA KONTROL
# ─────────────────────────────
if not check_admin_password():
    print("❌ Admin doğrulama başarısız")
    sys.exit(1)


# ─────────────────────────────
# SOCKET SERVER
# ─────────────────────────────
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # socket -> username

print(f"🟢 Server çalışıyor ({HOST}:{PORT})")


# ─────────────────────────────
# BROADCAST
# ─────────────────────────────
def broadcast(packet: dict):
    data = json.dumps(packet).encode()
    for c in list(clients.keys()):
        try:
            c.send(data)
        except:
            c.close()
            clients.pop(c, None)


# ─────────────────────────────
# CLIENT HANDLER
# ─────────────────────────────
def handle_client(conn):
    try:
        hello = json.loads(conn.recv(4096).decode())
        username = hello.get("from", "unknown")

        clients[conn] = username
        online_users.add(username)
        panel.set_users(list(online_users))

        print("➕ Bağlandı:", username)

        while True:
            raw = conn.recv(4096)
            if not raw:
                break

            msg = json.loads(raw.decode())

            if msg["type"] == "msg":
                text = decrypt(ROOM_KEY, msg["payload"])

                panel.add_chat(username, text)

                broadcast({
                    "type": "msg",
                    "from": username,
                    "payload": msg["payload"]
                })

    except Exception as e:
        print("❌ Client hata:", e)

    finally:
        name = clients.get(conn)
        if name:
            online_users.discard(name)
            panel.set_users(list(online_users))
            print("➖ Ayrıldı:", name)

        clients.pop(conn, None)
        conn.close()


# ─────────────────────────────
# ACCEPT LOOP
# ─────────────────────────────
def accept_loop():
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


threading.Thread(target=accept_loop, daemon=True).start()


# ─────────────────────────────
# ADMIN UI
# ─────────────────────────────
app = QApplication(sys.argv)
panel = AdminPanel()


def admin_send(text: str):
    encrypted = encrypt(ROOM_KEY, text)

    panel.add_chat("ADMIN", text)

    broadcast({
        "type": "msg",
        "from": "ADMIN",
        "payload": encrypted
    })


panel.send_message.connect(admin_send)
panel.show()

sys.exit(app.exec())
