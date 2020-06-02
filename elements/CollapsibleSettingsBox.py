from PyQt5.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, pyqtSlot
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
        self.content.setMinimumHeight(0)
        self.content.setMaximumHeight(0)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.toggle_animation = QParallelAnimationGroup(self)
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content, b"maximumHeight")
        )

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.content)


        self.choices = list()
        self.checked_choices = dict()
        self.set_list(self.data.get_areas()["Name"].tolist())
        self.setContentLayout(self.choice_list)

    @pyqtSlot()
    def action(self):
        checked = self.toggle.isChecked()
        self.toggle.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content.layout()
        del lay
        self.content.setLayout(layout)
        collapsed_height = (
                self.sizeHint().height() - self.content.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

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
