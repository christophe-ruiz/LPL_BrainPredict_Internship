from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from model import Modelling
from data import Data
from graph import Graph


class App(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.__verbose('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        self.__verbose('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def __set_inputs(self):
        self.__verbose('Setting input bar...')
        bar_layout = QHBoxLayout()
        bar = QWidget()
        bar.setLayout(bar_layout)
        widgets = []
        # TODO: Barre supérieure dans laquelle sont rangés les éléments suivants
        self.__verbose('Setting input labels...')
        # TODO: Label "Prediction file"
        self.__verbose('Setting input textfield...')
        # TODO: Textfield pour path du prediction file
        self.__verbose('Setting actions..')
        graph = QCheckBox()
        graph.setCheckState(Qt.Checked)
        graph.stateChanged.connect(lambda: self.__toggle_action('graph'))
        widgets.append(graph)
        
        model = QCheckBox()
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.__toggle_action('model'))
        widgets.append(model)
        self.__verbose('Adding widgets to input bar...')
        for w in widgets:
            bar_layout.addWidget(w)
        self.__verbose('Setting compute button...')
        compute = QPushButton()
        compute.setText("COMPUTE")
        compute.clicked.connect(lambda: self.__do_actions())

        self.__verbose('Adding bar to main widget...')
        self.main_layout.addWidget(bar)
        self.main_layout.addWidget(compute)

    def __compute_model(self):
        Modelling(data=self.data)

    def __compute_graph(self):
        Graph(data=self.data)

    def __do_actions(self):
        if self.action['graph']:
            self.__compute_graph()
        if self.action['model']:
            self.__compute_model()

    def __toggle_action(self, which):
        self.action[which] = not self.action[which]
        self.__verbose(which, 'is now', self.action[which])
    
    def __verbose(self, *args):
        # TODO: écrire le texte dans une barre de statut
        self.__verbose(*args)

    def __run(self):
        self.__verbose('Running app')
        self.show()
