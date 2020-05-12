from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    finished = pyqtSignal()
    msg = pyqtSignal(tuple)
