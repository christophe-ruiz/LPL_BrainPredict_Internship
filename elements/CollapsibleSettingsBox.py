from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, QToolButton, QSizePolicy, QVBoxLayout, QCheckBox
from PyQt5.QtCore import *


class CollapsibleSettingsBox(QWidget):
    def __init__(self):
        super().__init__()
        self.toggle = QToolButton()
        self.toggle.setCheckable(True)
        self.toggle.setText("Regions of Interest")
        self.toggle.setStyleSheet("{border: none;}")
        self.toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle.setArrowType(Qt.RightArrow)
        self.toggle.pressed.connect(lambda: self.action())

        self.choice_list = QVBoxLayout()

        self.content = QScrollArea()
        self.content.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.content.setMinimumSize(0, 0)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.content.setLayout(self.choice_list)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.content)

        self.set_list(['Test 1', 'Test 2'])
        self.checked_choices = dict()

    def action(self):
        checked = self.toggle.isChecked()
        self.toggle.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)

    def choice(self, option):
        self.checked_choices[option] = (True if option in self.checked_choices and not self.checked_choices[option] else False)
        print(self.checked_choices)

    def set_list(self, options):
        for o in options:
            c = QCheckBox(o)
            c.stateChanged.connect(lambda: self.choice(o))
            self.choice_list.addWidget(c)

