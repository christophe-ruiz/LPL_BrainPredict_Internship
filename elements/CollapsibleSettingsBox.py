from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, QToolButton, QSizePolicy, QVBoxLayout, QCheckBox


class CollapsibleSettingsBox(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
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

        self.choices = list()
        self.checked_choices = dict()
        self.set_list(self.data.get_areas()["Name"].tolist())

    def action(self):
        checked = self.toggle.isChecked()
        self.toggle.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)

    def choice(self):
        for c in self.choices:
            self.checked_choices[c.text()] = True if c.isChecked() else False
        print(self.checked_choices)

    def set_list(self, options):
        for o in options:
            c = QCheckBox(o)
            c.stateChanged.connect(lambda: self.choice())
            self.choices.append(c)
            self.choice_list.addWidget(c)

    def set_data(self, data):
        self.data = data
