import sys
import socket
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QMessageBox
)

HOST = "127.0.0.1"
PORT = 5000

class ChatWindow(QWidget):
    def __init__(self, username, client_socket):
        super().__init__()
        self.setWindowTitle(f"CryptoLANChat - {username}")
        self.setGeometry(400, 200, 600, 400)
        self.username = username
        self.client_socket = client_socket

        # Ana layout
        main_layout = QHBoxLayout()

        # Sol taraf: chat kutusu
        left_layout = QVBoxLayout()
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        left_layout.addWidget(self.chat_box)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Mesajınızı yazın...")
        left_layout.addWidget(self.entry)

        btn_layout = QHBoxLayout()
        self.send_button = QPushButton("Ortak Chat'e Gönder")
        self.send_button.clicked.connect(self.send_message)
        btn_layout.addWidget(self.send_button)

        self.dm_button = QPushButton("DM Gönder")
        self.dm_button.clicked.connect(self.send_dm)
        btn_layout.addWidget(self.dm_button)

        left_layout.addLayout(btn_layout)
        main_layout.addLayout(left_layout, 3)

        # Sağ taraf: kullanıcı listesi
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Kullanıcılar"))
        self.user_list = QListWidget()
        right_layout.addWidget(self.user_list)
        main_layout.addLayout(right_layout, 1)

        self.setLayout(main_layout)

        # Mesajları dinleme thread’i
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.entry.text().strip()
        if msg:
            # Ortak chat mesajı
            self.client_socket.sendall(msg.encode("utf-8"))
            self.chat_box.append(f"Sen (ortak): {msg}")
            self.entry.clear()

    def send_dm(self):
        msg = self.entry.text().strip()
        target_item = self.user_list.currentItem()
        if msg and target_item:
            target = target_item.text()
            dm_data = f"DM {target}:{msg}"
            self.client_socket.sendall(dm_data.encode("utf-8"))
            self.chat_box.append(f"Sen → {target} (DM): {msg}")
            self.entry.clear()
        else:
            QMessageBox.warning(self, "Hata", "DM için kullanıcı seçin ve mesaj yazın!")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                text = data.decode("utf-8")

                # Kullanıcı listesi güncellemesi
                if text.startswith("[USERS]"):
                    # Format: [USERS] user1,user2,user3
                    users = text.replace("[USERS]", "").strip().split(",")
                    self.user_list.clear()
                    for u in users:
                        if u.strip():
                            self.user_list.addItem(u.strip())
                else:
                    self.chat_box.append(text)
            except:
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Test için sahte socket (gerçekte login.py’den çağrılacak)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    w = ChatWindow("testuser", sock)
    w.show()
    sys.exit(app.exec())