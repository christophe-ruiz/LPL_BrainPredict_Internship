from app import App
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys


if __name__ == '__main__':
    # On crée une application thread-safe.
    app = QApplication([])
    app.setAttribute(Qt.AA_X11InitThreads)
    main = App()
    sys.exit(app.exec_())
