from PyQt5.QtWidgets import QMainWindow, QCheckBox
from PyQt5.QtCore import Qt, QObject


class App(QMainWindow):

    def __init__(self):
        self.action = {
            'graph': True,
            'model': True
        }
        super().__init__()
        self.set_infos()
        self.set_inputs()
        self.run()

    def set_infos(self):
        print('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        print('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def set_inputs(self):
        print('Setting input bar')
        # TODO: Barre supérieure dans laquelle sont rangés les éléments suivants
        print('Setting input labels')
        # TODO: Label "Prediction file"
        print('Setting input textfield')
        # TODO: Textfield pour path du prediction file
        print('Setting actions')
        graph = QCheckBox()
        graph.setCheckState(Qt.Checked)
        graph.stateChanged.connect(lambda: self.toggle_action('graph'))
        
        model = QCheckBox()
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.toggle_action('model'))

        # TODO: Ajouter le tout à la MainWindow.

    def compute_model(self):
        # TODO: Générer modélisation visbrain
        pass

    def compute_graph(self):
        # TODO: Générer graphique matplotlib
        pass

    def toggle_action(self, which):
        self.action[which] = not self.action[which]
        print(which, 'is now', self.action[which])

    def run(self):
        print('Running app')
        self.show()
