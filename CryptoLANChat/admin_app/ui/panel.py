from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Signal


class AdminPanel(QWidget):
    send_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.resize(800, 500)

        main = QHBoxLayout(self)

        # ── Users
        self.users = QListWidget()
        self.users.setFixedWidth(200)

        # ── Chat
        chat_layout = QVBoxLayout()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Admin mesajı...")

        send_btn = QPushButton("Gönder")
        send_btn.clicked.connect(self._send)

        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(send_btn)

        chat_layout.addWidget(QLabel("Chat"))
        chat_layout.addWidget(self.chat)
        chat_layout.addLayout(bottom)

        main.addWidget(self.users)
        main.addLayout(chat_layout)

    def _send(self):
        text = self.input.text().strip()
        if text:
            self.send_message.emit(text)
            self.input.clear()

    def add_chat(self, sender, text):
        self.chat.append(f"<b>{sender}:</b> {text}")

    def set_users(self, users: list):
        self.users.clear()
        self.users.addItems(users)
