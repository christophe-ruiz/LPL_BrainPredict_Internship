from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, \
    QVBoxLayout, QHBoxLayout, QWidget, QStatusBar, QTabWidget, QFileDialog
from PyQt5.QtCore import Qt

from data import Data
from task_thread import ModellingThread, GraphThread
from tab_widget import SettingsWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = {
            'graph': True,
            'modelling': True
        }
        self.data = Data(predictions='./data/predictions.csv',
                         areas='./data/brain_areas.tsv',
                         left='./parcellation/lh.BN_Atlas.annot',
                         right='./parcellation/rh.BN_Atlas.annot')
        self.__set_infos()
        self.main_layout = QVBoxLayout()
        self.main = QTabWidget()
        self.main.addTab(SettingsWidget(self), "Settings")
        self.main.setLayout(self.main_layout)
        self.setCentralWidget(self.main)
        self.__run()

    def __set_infos(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.verbose('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        self.verbose('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def __compute_model(self):
        self.modelTh = ModellingThread(self, data=self.data)
        self.modelTh.start()

    def __compute_graph(self):
        self.graphTh = GraphThread(self, data=self.data)
        self.graphTh.start()

    def do_actions(self):
        if self.action['graph']:
            self.__compute_graph()
        if self.action['modelling']:
            self.__compute_model()

    def toggle_action(self, which):
        self.action[which] = not self.action[which]
        if self.action[which]:
            self.verbose('Predictions will be computed as a', which)
        else:
            self.verbose('Predictions will not be computed as a', which)
    
    def verbose(self, *args):
        self.statusBar.showMessage(' '.join(map(str, args)), 5000)
        print(*args)

    def get_path(self):
        predictions_path, _ = QFileDialog.getOpenFileName(self, 'Open prediction file', filter="CSV files (*.csv)")
        self.verbose('Selected file :', predictions_path)
        self.data.set_predictions(predictions_path)

    def __run(self):
        self.show()
        self.verbose('App started')
