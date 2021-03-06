from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ntpath

"""
Widget contenant les boutons de sélection des fichiers audio et vidéo d'entrée.
"""


class InputMediaBox(QWidget):
    def __init__(self, app, **kwargs):
        super(InputMediaBox, self).__init__()
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: white")
        self.app = app
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.buttons = dict()
        self.buttons_text = dict()
        for filename, filetype in kwargs.items():
            title = ' '.join(filename.split('_'))
            file_box = QGroupBox(title.capitalize() + " file")
            file_box.setAutoFillBackground(True)
            file_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            file_box.setStyleSheet("background-color: white")

            btn = QPushButton('Choose file', self)
            btn.setStatusTip('Choose the input ' + title + ' path.')
            btn.clicked.connect(lambda _, fname=filename, ftype=filetype : self.get_input_file(fname, ftype))

            text = QLabel()
            text.setText('Path: ')

            self.buttons[filename] = filetype
            self.buttons_text[filename] = text

            box_layout = QVBoxLayout(file_box)
            box_layout.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(btn)
            box_layout.addWidget(text)

            self.layout.addWidget(file_box)

    def get_input_file(self, fname, ftype):
        path = self.app.get_input_path(fname, ftype)
        if path is not None:
            _, path = ntpath.split(path)
            self.buttons_text[fname].setText("Path: " + path)
        else:
            self.buttons_text[fname].setText("Path: ")

