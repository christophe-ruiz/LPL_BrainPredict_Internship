from app import App
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
import sys


if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_X11InitThreads)
    main = App()
    sys.exit(app.exec_())
