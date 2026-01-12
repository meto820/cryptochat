import sys
from PySide6.QtWidgets import QApplication
from client_app.ui.login import LoginWindow

app = QApplication(sys.argv)
win = LoginWindow()
win.show()
sys.exit(app.exec())
