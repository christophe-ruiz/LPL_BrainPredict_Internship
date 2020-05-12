from PyQt5.QtCore import pyqtSignal, QObject

"""
Signaux utilisés pour gérer les threads.
"""
class Signals(QObject):
    # à utiliser pour indiquer la fin d'une tâche
    finished = pyqtSignal()
    # à utiliser pour envoyer un message au parent.
    msg = pyqtSignal(tuple)
