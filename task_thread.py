from PyQt5.QtCore import QThread
from model import Modelling
from graph import Graph


class ModellingThread(QThread):
    def __init__(self, app, data):
        super(ModellingThread, self).__init__()
        self.data = data
        self.app = app

    def run(self) -> None:
        Modelling(self.app, self.data)


class GraphThread(QThread):
    def __init__(self, app, data):
        super(GraphThread, self).__init__()
        self.data = data
        self.app = app

    def run(self) -> None:
        Graph(self.app, self.data)
