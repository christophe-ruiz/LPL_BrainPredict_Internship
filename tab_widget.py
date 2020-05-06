from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QGroupBox, QSizePolicy, QVBoxLayout


class SettingsWidget(QWidget):
    def __init__(self, app):
        super(SettingsWidget, self).__init__()
        self.app = app
        self.__set_inputs()

    def __set_inputs(self):
        self.app.verbose('Setting input bar...')
        settings_box = QGroupBox("Compute data as...")
        settings_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        bar_layout = QHBoxLayout()
        settings_box.setLayout(bar_layout)

        self.app.verbose('Setting input textfield...')
        file_box = QGroupBox("Prediction file")
        file_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        path_btn = QPushButton('Choose file', self)
        path_btn.setStatusTip('Choose prediction file')
        path_btn.clicked.connect(self.app.get_path)

        file_layout = QVBoxLayout()
        file_layout.addWidget(path_btn)
        file_box.setLayout(file_layout)

        self.app.verbose('Setting action checkboxes...')
        widgets = []

        graph = QCheckBox("Graph")
        graph.setCheckState(Qt.Checked)
        graph.stateChanged.connect(lambda: self.app.toggle_action('graph'))
        widgets.append(graph)

        model = QCheckBox("Modelling")
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.app.toggle_action('modelling'))
        widgets.append(model)

        self.app.verbose('Adding widgets to input bar...')
        for w in widgets:
            bar_layout.addWidget(w)

        self.app.verbose('Setting compute button...')
        compute = QPushButton("COMPUTE")
        compute.clicked.connect(lambda: self.app.do_actions())

        self.app.verbose('Adding widget to settings tab...')
        self.app.main_layout.addWidget(file_box)
        self.app.main_layout.addWidget(settings_box)
        self.app.main_layout.addWidget(compute)



class GraphOutWidget(QWidget):
    def __init__(self, app):
        super(GraphOutWidget, self).__init__()



class ModelingOutWidget(QWidget):
    def __init__(self, app):
        super(ModelingOutWidget, self).__init__()

