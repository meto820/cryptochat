import socket
import threading
import json

from share.crypto import encrypt, decrypt
from client_app.config import SERVER_IP, PORT, ROOM_KEY, USERNAME


# ───────── CONNECT ─────────
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


# ───────── HELLO (ZORUNLU) ─────────
hello = {
    "type": "hello",
    "from": USERNAME
}
client.send(json.dumps(hello).encode())


# ───────── RECEIVE THREAD ─────────
def receive():
    while True:
        try:
            raw = client.recv(4096)
            if not raw:
                break

            msg = json.loads(raw.decode())

            if msg.get("type") == "msg":
                text = decrypt(ROOM_KEY, msg["payload"])
                print(f"\n[{msg['from']}] {text}\n> ", end="")

        except Exception as e:
            print("\n❌ Bağlantı kesildi:", e)
            break


threading.Thread(target=receive, daemon=True).start()


# ───────── SEND LOOP ─────────
print("💬 Mesaj yaz (çıkmak için Ctrl+C)")

while True:
    try:
        text = input("> ")

        encrypted = encrypt(ROOM_KEY, text)

        packet = {
            "type": "msg",
            "from": USERNAME,
            "payload": encrypted
        }

        client.send(json.dumps(packet).encode())

    except KeyboardInterrupt:
        print("\n👋 Çıkılıyor")
        client.close()
        break
