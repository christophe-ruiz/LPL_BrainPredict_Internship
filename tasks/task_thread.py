from PyQt5.QtCore import QRunnable, pyqtSlot
from tasks.model import Modeling
from tasks.graph import Graph
from tasks.signals import Signals

# TODO: Refactoriser pour n'avoir qu'une classe.
"""
Permet la construction de la modélisation dans un thread
"""


class ModelingThread(QRunnable):
    def __init__(self, data):
        super(ModelingThread, self).__init__()
        self.data = data
        self.signals = Signals()

    """
    Renvoie les messages du signal msg au parent.
    """
    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        m = Modeling(self.data)
        m.signals.msg.connect(self.repeat_msg)
        m.signals.finished.connect(lambda: self.signals.finished.emit())
        m.start()


"""
Permet la construction du graphique dans un thread
"""


class GraphThread(QRunnable):
    def __init__(self, data):
        super(GraphThread, self).__init__()
        self.data = data
        self.signals = Signals()

    """
    Renvoie les messages du signal msg au parent.
    """
    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        g = Graph(self.data)
        g.signals.msg.connect(self.repeat_msg)
        g.signals.finished.connect(lambda: self.signals.finished.emit())
        g.start()
