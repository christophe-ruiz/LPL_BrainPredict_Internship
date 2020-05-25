from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class InputMediaBox(QWidget):
    def __init__(self, app, **kwargs):
        self.app = app
        super(InputMediaBox, self).__init__()
        self.layout = QVBoxLayout(self)
        for filename, filetype in kwargs.items():
            btn = QPushButton('Choose file', self)
            btn.setStatusTip('Choose the input ' + filename + ' file.')
            btn.clicked.connect(lambda: self.app.get_input_file(filename, filetype))
            self.layout.addWidget(btn)
