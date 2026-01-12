from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoLANChat - Giriş")
        self.setFixedSize(320, 300)

        layout = QVBoxLayout()

        title = QLabel("🔐 CryptoLANChat")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı adı")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Parola")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = QPushButton("Giriş Yap")
        self.register_btn = QPushButton("Kayıt Ol")

        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

        # Button actions
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldur")
            return

        QMessageBox.information(
            self, "Başarılı", f"Giriş OK\nKullanıcı: {username}"
        )

    def register(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldur")
            return

        QMessageBox.information(
            self, "Kayıt", f"Kayıt OK\nKullanıcı: {username}"
        )
