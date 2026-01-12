from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

from admin_app.auth import check_or_create_admin


class AdminLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Girişi")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Admin Parolası"))

        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Giriş")

        layout.addWidget(self.pw)
        layout.addWidget(btn)

        btn.clicked.connect(self.login)

    def login(self):
        if check_or_create_admin(self.pw.text()):
            QMessageBox.information(self, "OK", "Admin girişi başarılı")
            from admin_app.ui.panel import AdminPanel
            self.panel = AdminPanel()
            self.panel.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Parola yanlış")
