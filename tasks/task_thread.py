from PyQt5.QtCore import QRunnable, pyqtSlot
from tasks.model import Modeling
from tasks.graph import Graph
from tasks.generate_ts import GenerateTimeSeries
from tasks.predict import Predict
from tasks.signals import Signals

# TODO: Refactoriser pour n'avoir qu'une classe ?
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


class GenerateTimeSeriesThread(QRunnable):
    def __init__(self, regions, openface_path, pred_module_path, input_dir, video_path, language="fr"):
        super(GenerateTimeSeriesThread, self).__init__()
        self.regions = regions
        self.openface_path = openface_path
        self.pred_module_path = pred_module_path
        self.input_dir = input_dir
        self.video_path = video_path
        self.language = language
        self.signals = Signals()

    """
    Renvoie les messages du signal msg au parent.
    """

    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        g = GenerateTimeSeries(self.regions,
                               self.openface_path,
                               self.pred_module_path,
                               self.input_dir,
                               self.video_path,
                               self.language)
        g.signals.msg.connect(self.repeat_msg)
        g.signals.finished.connect(lambda: self.signals.finished.emit())
        g.start()


class PredictThread(QRunnable):
    def __init__(self, regions, type, pred_module_path, input_dir, lag):
        super(PredictThread, self).__init__()
        self.regions = regions
        self.type = type
        self.lag = lag
        self.pred_module_path = pred_module_path
        self.input_dir = input_dir
        self.signals = Signals()

    """
    Renvoie les messages du signal msg au parent.
    """

    def repeat_msg(self, msg):
        self.signals.msg.emit(msg)

    @pyqtSlot()
    def run(self) -> None:
        p = Predict(self.regions,
                    self.type,
                    self.pred_module_path,
                    self.input_dir,
                    self.lag)
        p.signals.msg.connect(self.repeat_msg)
        p.signals.finished.connect(lambda: self.signals.finished.emit())
        p.start()