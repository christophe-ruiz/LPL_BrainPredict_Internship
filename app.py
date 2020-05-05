from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt5.QtCore import Qt

from data import Data
from task_thread import ModellingThread, GraphThread


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text = ''
        self.action = {
            'graph': True,
            'model': True
        }
        self.data = Data(predictions='./data/predictions.csv',
                         areas='./data/brain_areas.tsv',
                         left='./parcellation/lh.BN_Atlas.annot',
                         right='./parcellation/rh.BN_Atlas.annot')
        self.main_layout = QVBoxLayout()
        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        self.__set_infos()
        self.__set_inputs()
        self.setCentralWidget(self.main)
        self.__run()

    def __set_infos(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.verbose('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        self.verbose('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def __set_inputs(self):
        self.verbose('Setting input bar...')
        bar_layout = QHBoxLayout()
        bar = QWidget()
        bar.setLayout(bar_layout)
        widgets = []
        # TODO: Barre supérieure dans laquelle sont rangés les éléments suivants
        self.verbose('Setting input labels...')
        # TODO: Label "Prediction file"
        self.verbose('Setting input textfield...')
        # TODO: Textfield pour path du prediction file
        self.verbose('Setting actions..')
        graph = QCheckBox()
        graph.setCheckState(Qt.Checked)
        graph.stateChanged.connect(lambda: self.__toggle_action('graph'))
        widgets.append(graph)
        
        model = QCheckBox()
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.__toggle_action('model'))
        widgets.append(model)
        self.verbose('Adding widgets to input bar...')
        for w in widgets:
            bar_layout.addWidget(w)
        self.verbose('Setting compute button...')
        compute = QPushButton("COMPUTE")
        compute.clicked.connect(lambda: self.__do_actions())

        self.verbose('Adding bar to main widget...')
        self.main_layout.addWidget(bar)
        self.main_layout.addWidget(compute)

    def __compute_model(self):
        self.modelTh = ModellingThread(self, data=self.data)
        self.modelTh.start()

    def __compute_graph(self):
        self.graphTh = GraphThread(self, data=self.data)
        self.graphTh.start()

    def __do_actions(self):
        if self.action['graph']:
            self.__compute_graph()
        if self.action['model']:
            self.__compute_model()

    def __toggle_action(self, which):
        self.action[which] = not self.action[which]
        if self.action[which]:
            self.verbose('Predictions will be computed as a', which)
        else:
            self.verbose('Predictions will not be computed as a', which)
    
    def verbose(self, *args):
        self.statusBar.showMessage(' '.join(map(str, args)), 5000)
        print(*args)

    def __run(self):
        self.verbose('Running app')
        self.show()
