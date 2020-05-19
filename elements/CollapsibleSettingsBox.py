from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, QToolButton, QSizePolicy, QVBoxLayout
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

        self.content = QScrollArea()
        self.content.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.content.setMinimumSize(0, 0)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.content)

    def action(self):
        checked = self.toggle.isChecked()
        self.toggle.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        print('click')
