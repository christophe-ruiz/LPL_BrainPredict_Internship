from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QObject

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
        self.data = Data(left='./parcellation/lh.BN_Atlas.annot',
                         right='./parcellation/rh.BN_Atlas.annot')
        self.main = QVBoxLayout()

        self.__set_infos()
        self.__set_inputs()
        self.__run()

    def __set_infos(self):
        print('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        print('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def __set_inputs(self):
        print('Setting input bar...')
        bar = QHBoxLayout()
        widgets = []
        # TODO: Barre supérieure dans laquelle sont rangés les éléments suivants
        print('Setting input labels...')
        # TODO: Label "Prediction file"
        print('Setting input textfield...')
        # TODO: Textfield pour path du prediction file
        print('Setting actions..')
        graph = QCheckBox()
        graph.setCheckState(Qt.Checked)
        graph.stateChanged.connect(lambda: self.__toggle_action('graph'))
        widgets.append(graph)
        
        model = QCheckBox()
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.__toggle_action('model'))
        widgets.append(model)
        print('Adding widgets to input bar...')
        for w in widgets:
            bar.addWidget(w)
        print('Setting compute button...')
        compute = QPushButton()
        compute.isCheckable(True)
        compute.setText("COMPUTE")
        compute.clicked.connect(lambda: self.__do_actions())

        print('Adding bar to main widget...')
        self.main.addWidget(bar)

    def __compute_model(self):
        md = Modelling(self.data)

    def __compute_graph(self):
        gr = Graph(self.data)

    def __do_actions(self):
        if self.action['graph']:
            self.__compute_graph()
        if self.action['model']:
            self.__compute_model()

    def __toggle_action(self, which):
        self.action[which] = not self.action[which]
        print(which, 'is now', self.action[which])

    def __run(self):
        print('Running app')
        self.show()
