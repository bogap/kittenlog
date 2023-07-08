from PyQt6.QtWidgets import QApplication
import sys
from app.backend.windows import Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
