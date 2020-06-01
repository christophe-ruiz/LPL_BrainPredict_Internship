from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ntpath


class InputMediaBox(QWidget):
    def __init__(self, app, **kwargs):
        self.app = app
        super(InputMediaBox, self).__init__()
        self.layout = QVBoxLayout(self)
        self.buttons = dict()
        self.buttons_text = dict()
        for filename, filetype in kwargs.items():
            file_box = QGroupBox(filename.capitalize() + " file")
            file_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            btn = QPushButton('Choose file', self)
            btn.setStatusTip('Choose the input ' + filename + ' file.')
            btn.clicked.connect(lambda _, fname=filename, ftype=filetype : self.get_input_file(fname, ftype))

            text = QLabel()
            text.setText('File: ')

            self.buttons[filename] = filetype
            self.buttons_text[filename] = text

            box_layout = QVBoxLayout(file_box)
            box_layout.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(btn)
            box_layout.addWidget(text)

            self.layout.addWidget(file_box)

    def get_input_file(self, fname, ftype):
        path = self.app.get_input_file(fname, ftype)
        if path is not None:
            _, path = ntpath.split(path)
            self.buttons_text[fname].setText("File: " + path)
        else:
            self.buttons_text[fname].setText("File: ")

