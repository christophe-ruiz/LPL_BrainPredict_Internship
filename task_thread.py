from PyQt5.QtCore import QThread
from model import Modeling
from graph import Graph


class ModelingThread(QThread):
    def __init__(self, app, data):
        super(ModelingThread, self).__init__()
        self.data = data
        self.app = app

    def run(self) -> None:
        Modeling(self.app, self.data)


class GraphThread(QThread):
    def __init__(self, app, data):
        super(GraphThread, self).__init__()
        self.data = data
        self.app = app

    def run(self) -> None:
        Graph(self.app, self.data)
