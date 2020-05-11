from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QGroupBox, QSizePolicy, QVBoxLayout, QStyle,\
    QSlider


class SettingsWidget(QWidget):
    def __init__(self, app):
        super(SettingsWidget, self).__init__()
        self.app = app

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
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

        model = QCheckBox("Modeling")
        model.setCheckState(Qt.Checked)
        model.stateChanged.connect(lambda: self.app.toggle_action('modeling'))
        widgets.append(model)

        self.app.verbose('Adding widgets to input bar...')
        for w in widgets:
            bar_layout.addWidget(w)

        self.app.verbose('Setting compute button...')
        compute = QPushButton("COMPUTE")
        compute.clicked.connect(lambda: self.app.do_actions())

        self.app.verbose('Adding widget to settings tab...')
        self.layout.addWidget(file_box)
        self.layout.addWidget(settings_box)
        self.layout.addWidget(compute)


class VideoPlayer(QWidget):
    def __init__(self, video_path):
        super(VideoPlayer, self).__init__()
        self.player = QMediaPlayer(flags=QMediaPlayer.VideoSurface)
        self.video = QVideoWidget()

        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.setEnabled(False)
        self.playBtn.clicked.connect(self.play)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(lambda pos: self.player.setPosition(pos))

        self.controls = QHBoxLayout()
        self.controls.addWidget(self.playBtn)
        self.controls.addWidget(self.slider)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video)
        self.layout.addLayout(self.controls)

        self.player.setVideoOutput(self.video)
        self.player.stateChanged.connect(self.change_state)
        self.player.positionChanged.connect(lambda pos: self.slider.setValue(pos))
        self.player.durationChanged.connect(lambda duration: self.slider.setRange(0, duration))

        self.setLayout(self.layout)

        if video_path.strip() != '':
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.playBtn.setEnabled(True)
            self.play()

    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def change_state(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
