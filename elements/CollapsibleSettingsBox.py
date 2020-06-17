"""
Widget contenant les regions exploitables sous formes de cases à cocher pour selectionner les regions
à calculer pour la reprséentation des données sous forme d'animation ou de graphique.

adapté de la version de PyQt4 proposée ici : https://github.com/By0ute/pyqt-collapsible-widget
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox


class CollapsibleSettingsBox(QWidget):
    def __init__(self, btn_titles, parent=None, title=None):
        QFrame.__init__(self, parent=parent)
        super().__init__(parent)

        self._is_collapsed = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collapsed))
        self._main_v_layout.addWidget(self.initContent(self._is_collapsed))

        self.initCollapsable()

        self.choice_btns = list()

        for title in btn_titles:
            btn = QCheckBox(title)
            btn.stateChanged.connect(lambda: self.choices())
            self.choice_btns.append(btn)
            self.addWidget(btn)

    def choices(self):
        i = 0
        checked_choices = ""
        for c in self.choice_btns:
            i = i + 1
            if c.isChecked():
                checked_choices = checked_choices + str(i)
        print(checked_choices)
        return checked_choices

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QWidget()
        self._content_layout = QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        self._title_frame.clicked.connect(lambda: self.toggleCollapsed())

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collapsed)
        self._is_collapsed = not self._is_collapsed
        self._title_frame.arrow().setArrow(int(self._is_collapsed))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QFrame):
        clicked = pyqtSignal()

        def __init__(self, parent=None, title="", collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))
            self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def arrow(self):
            return self._arrow

        def initArrow(self, collapsed):
            self._arrow = CollapsibleSettingsBox.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QtCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            self.clicked.emit()

            return super(CollapsibleSettingsBox.TitleFrame, self).mousePressEvent(event)

    #############################
    #           ARROW           #
    #############################
    class Arrow(QFrame):
        def __init__(self, parent=None, collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal
            # self.paintEvent()

        def paintEvent(self, event):
            print(self._arrow)
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setBrush(QtGui.QColor(192, 192, 192))
            painter.setPen(QtGui.QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()
