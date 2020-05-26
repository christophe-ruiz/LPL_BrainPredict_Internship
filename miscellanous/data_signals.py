from PyQt5.QtCore import pyqtSignal, QObject

"""
Signaux utilisés pour gérer les changements de valeurs des instances de la classe Data
"""


class DataSignals(QObject):
    audio = pyqtSignal(str)
    video = pyqtSignal(str)
