from PyQt5.QtCore import QRunnable, pyqtSlot
from model import Modeling
from graph import Graph
from signals import Signals


class ModelingThread(QRunnable):
    def __init__(self, data):
        super(ModelingThread, self).__init__()
        self.data = data
        self.signals = Signals()

    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        m = Modeling(self.data)
        m.signals.msg.connect(self.repeat_msg)
        m.start()
        self.signals.finished.emit()


class GraphThread(QRunnable):
    def __init__(self, data):
        super(GraphThread, self).__init__()
        self.data = data
        self.signals = Signals()

    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        g = Graph(self.data)
        g.signals.msg.connect(self.repeat_msg)
        g.start()
        self.signals.finished.emit()
