import sys
import socket
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt

HOST = "127.0.0.1"   # Server IP (LAN'da server'ın IP'sini yaz)
PORT = 5000          # Server port

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoLANChat - Client (PySide6)")
        self.setGeometry(300, 200, 400, 300)

        # Socket bağlantısı
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            print(f"[client] Bağlantı hatası: {e}")
            sys.exit(1)

        # UI Layout
        layout = QVBoxLayout()

        self.label = QLabel(f"Bağlı: {HOST}:{PORT}")
        layout.addWidget(self.label)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Mesajınızı yazın...")
        layout.addWidget(self.entry)

        self.send_button = QPushButton("Gönder")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        # Mesajları dinleyen thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.entry.text().strip()
        if msg:
            try:
                self.client_socket.sendall(msg.encode("utf-8"))
                self.chat_box.append(f"Sen: {msg}")
                self.entry.clear()
            except Exception as e:
                self.chat_box.append(f"[client] Gönderim hatası: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    self.chat_box.append(data.decode("utf-8"))
            except Exception:
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatClient()
    window.show()
    sys.exit(app.exec())