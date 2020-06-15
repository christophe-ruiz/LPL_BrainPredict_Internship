from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QGroupBox, QSizePolicy, QVBoxLayout, QStyle, \
    QSlider, QGridLayout, QComboBox
from elements.CollapsibleSettingsBox import CollapsibleSettingsBox
from elements.InputMediaBox import InputMediaBox
from tasks.task_thread import GenerateTimeSeriesThread, PredictThread


class SettingsWidget(QWidget):
    def __init__(self, app):
        super(SettingsWidget, self).__init__()
        self.app = app
        self.conversation_type = 'h'
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.app.verbose('Setting input bar...')
        settings_box = QGroupBox("Compute data as...")
        settings_box.setAutoFillBackground(True)
        settings_box.setStyleSheet("background-color: white")
        bar_layout = QHBoxLayout()
        settings_box.setLayout(bar_layout)

        self.app.verbose('Setting input textfield...')
        file_box = QGroupBox("Prediction file")
        file_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        path_btn = QPushButton('Choose file', self)
        path_btn.setStatusTip('Choose prediction file')
        path_btn.clicked.connect(self.app.get_path)

        file_layout = QVBoxLayout()
        file_layout.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(path_btn)
        file_box.setLayout(file_layout)
        file_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        human_or_robot = QComboBox()
        human_or_robot.addItems(["Human-Human", "Human-Robot"])
        human_or_robot.currentIndexChanged.connect(lambda: self.select_conversation_type(human_or_robot.currentText()))

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

        generate = QPushButton("GENERATE TIME SERIES")
        generate.clicked.connect(lambda: self.generate_time_series())

        test_predict = QPushButton("TEST PREDICT")
        test_predict.clicked.connect(lambda: self.compute_predictions())

        name_list = self.app.get_data().get_areas()["Name"].tolist()
        self.region_selector = CollapsibleSettingsBox(name_list, title="Regions of Interest")

        self.input_paths_kw = dict(
            working_directory="Working directory (dir)",
            open_face_directory="Open face directory (dir)",
            audio="Audio directory (dir)",
            video="Video file (*.avi)"
        )
        general_keys = ['working_directory', 'open_face_directory']
        general_kw = {k: v for k, v in self.input_paths_kw.items() if k in general_keys}

        media_keys = ['audio', 'video']
        media_kw = {k: v for k, v in self.input_paths_kw.items() if k in media_keys}

        input_general = InputMediaBox(self.app, **general_kw)
        input_media = InputMediaBox(self.app, **media_kw)

        self.app.verbose('Adding widget to settings tab...')
        self.layout.addWidget(input_general, 0, 0)
        self.layout.addWidget(input_media, 0, 1)
        self.layout.addWidget(self.region_selector, 1, 0, 3, 1, Qt.AlignCenter)
        self.layout.addWidget(human_or_robot, 3, 0)
        self.layout.addWidget(file_box, 1, 1)
        self.layout.addWidget(settings_box, 2, 1)
        self.layout.addWidget(compute, 3, 1)
        self.layout.addWidget(generate, 4, 1)
        self.layout.addWidget(test_predict, 5, 1)

    def check_paths(self):
        for path in self.input_paths_kw:
            if path not in self.app.paths:
                self.app.verbose(" /!\ Missing path for ", ' '.join(self.input_paths_kw[path].split(" ")[:-1]))
                return False
            elif self.app.paths[path][-1] == '/':
                self.app.paths[path] = self.app.paths[path][:-1]
        return True

    def select_conversation_type(self, conv_type):
        if conv_type == 'Human-Human':
            self.conversation_type = 'h'
        elif conv_type == 'Human-Robot':
            self.conversation_type = 'r'
        self.app.verbose(self.conversation_type)

    def generate_time_series(self):
        if not self.check_paths():
            return
        # gts_th est un thread destiné à créer les séries temporelles.
        gts_th = GenerateTimeSeriesThread(self.region_selector.choices(),
                                          self.app.paths["open_face_directory"],
                                          self.app.paths["working_directory"] + "/PredictionModule",
                                          self.app.paths["working_directory"],
                                          self.app.paths["video"],
                                          self.app.paths["audio"]
                                          )
        # Les messages reçus par le signal "msg" seront traités par verbose pour les afficher.
        gts_th.signals.msg.connect(lambda msg: self.app.verbose(*msg))
        # Une fois le travail fini, on l'écrit dans la barre de statut
        gts_th.signals.finished.connect(lambda: self.app.verbose("Time series successfully generated."))
        # On demande à threadpool de lancer le thread.
        self.app.threadpool.start(gts_th)

    def compute_predictions(self):
        # pred_th est un thread destiné à créer les prédictions.
        pred_th = PredictThread(self.region_selector.choices(),
                                self.conversation_type,
                                self.app.paths["working_directory"] + "/PredictionModule",
                                self.app.paths["working_directory"],
                                6
                                )
        # Les messages reçus par le signal "msg" seront traités par verbose pour les afficher.
        pred_th.signals.msg.connect(lambda msg: self.app.verbose(*msg))
        # Une fois le travail fini, on l'écrit dans la barre de statut
        pred_th.signals.finished.connect(lambda: self.app.verbose("Predictions successfully generated."))
        # On demande à threadpool de lancer le thread.
        self.app.threadpool.start(pred_th)


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
