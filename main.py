from app import App
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication([])
    main = App()
    sys.exit(app.exec_())
