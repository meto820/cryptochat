import sys
import socket
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)

HOST = "127.0.0.1"   # Server IP
PORT = 5000          # Server port

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoLANChat - Login/Register")
        self.setGeometry(400, 200, 300, 200)

        layout = QVBoxLayout()

        self.label_user = QLabel("Kullanıcı Adı:")
        layout.addWidget(self.label_user)

        self.username_entry = QLineEdit()
        layout.addWidget(self.username_entry)

        self.label_pass = QLabel("Şifre:")
        layout.addWidget(self.label_pass)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Kayıt Ol")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        self.authenticate("LOGIN")

    def register(self):
        self.authenticate("REGISTER")

    def authenticate(self, mode):
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre giriniz!")
            return

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))

            # Server’dan gelen ilk mesajları oku
            welcome1 = client_socket.recv(1024).decode("utf-8")
            welcome2 = client_socket.recv(1024).decode("utf-8")
            print(welcome1.strip(), welcome2.strip())

            # Giriş veya kayıt isteğini gönder
            login_data = f"{mode} {username}:{password}"
            client_socket.sendall(login_data.encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")
            if "Hoş geldiniz" in response or "Kayıt başarılı" in response:
                self.chat = ChatWindow(username, client_socket)
                self.chat.show()
                self.close()
            else:
                QMessageBox.warning(self, "Hata", response.strip())
                client_socket.close()
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", str(e))

class ChatWindow(QWidget):
    def __init__(self, username, client_socket):
        super().__init__()
        self.setWindowTitle(f"CryptoLANChat - {username}")
        self.setGeometry(400, 200, 400, 300)
        self.username = username
        self.client_socket = client_socket

        layout = QVBoxLayout()

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

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.entry.text().strip()
        if msg:
            self.client_socket.sendall(msg.encode("utf-8"))
            self.chat_box.append(f"Sen: {msg}")
            self.entry.clear()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    self.chat_box.append(data.decode("utf-8"))
            except:
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())