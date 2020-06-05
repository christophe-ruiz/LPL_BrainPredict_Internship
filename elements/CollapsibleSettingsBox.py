from PyQt5.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, QToolButton, QSizePolicy, QVBoxLayout, QCheckBox

"""
Widget contenant les regions exploitables sous formes de cases à cocher pour selectionner les regions
à calculer pour la reprséentation des données sous forme d'animation ou de graphique.
"""
# TODO: Récupérer les regions dynamiquement à partir du fichier de prédiction généré, pas de celui existant
#  dans les ressources.


class CollapsibleSettingsBox(QWidget):
    def __init__(self, data):
        super(CollapsibleSettingsBox, self).__init__()
        # Contient le chemin du fichier de prédictions contenant les label des régions
        self.data = data
        # Bouton pour dérouler le menu
        self.toggle = QToolButton()
        self.toggle.setCheckable(True)
        self.toggle.setText("Regions of Interest")
        self.toggle.setStyleSheet("{border: none;}")
        self.toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle.setArrowType(Qt.RightArrow)
        self.toggle.pressed.connect(lambda: self.action())

        # Layout contenant les cases à cocher
        self.choice_list = QVBoxLayout()

        # Widget contenant les cases à cocher
        self.content = QScrollArea()
        self.content.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.content.setMinimumHeight(0)
        self.content.setMaximumHeight(0)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        #  Animation à réaliser au déroulement du menu
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

        # Layout contenant les éléments du menu.
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
        # On regarde si le menu est ouvert / fermé.
        checked = self.toggle.isChecked()
        # On change la fleche du bouton en conséquence.
        self.toggle.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        # On réalise l'animation dans le sens correspondant.
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        # On supprime le layout existant s'il y en a un.
        lay = self.content.layout()
        del lay
        # On met en place le layout.
        layout.addStretch()
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
        # On regarde l'état des cases pour les enregistrer.
        for c in self.choices:
            self.checked_choices[c.text()] = True if c.isChecked() else False
        print(self.checked_choices)

    def set_list(self, options):
        # On ajoute les options passées en parametre.
        for o in options:
            c = QCheckBox(o)
            c.stateChanged.connect(lambda: self.choice())
            self.choices.append(c)
            self.choice_list.addWidget(c)

    def set_data(self, data):
        self.data = data
