from PyQt5.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QFileDialog
from PyQt5.QtCore import QThreadPool

from miscellanous.data import Data
from tasks.task_thread import ModelingThread, GraphThread
from settings_widget import SettingsWidget, VideoPlayer

import os
import subprocess

"""
Application PyQt5 contenant les éléments de l'interface.
"""
class App(QMainWindow):
    """
    Initialisation de la fenêtre principale contenant le tabwidget.
    """
    def __init__(self):
        super().__init__()
        # Contient les chemins utiles au fonctionnement des fonctionnalités (peut-être redondant avec data)
        # OpenFace, Working directory, audio input, video input
        self.paths = dict()
        # Contient les choix des contenu à générer, ils sont préselectionnés.
        self.action = {
            'graph': True,
            'modeling': True
        }
        # Contient des chemins pour les fonctionnalités
        self.data = Data(predictions='./data/predictions.csv',
                         areas='./data/brain_areas.tsv',
                         left='./parcellation/lh.BN_Atlas.annot',
                         right='./parcellation/rh.BN_Atlas.annot')
        # threadpool sera le gestionnaire des threads executant les tâches de modelisation et de création du graphique.
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)
        self.__set_infos()

        # widget à onglets
        self.main = QTabWidget()
        self.main.addTab(SettingsWidget(self), "Settings")

        self.setCentralWidget(self.main)

        self.__run()

    """
    Mise en place de la barre de statut, de la position initiale et du titre.
    """
    def __set_infos(self):
        # Barre de statut qui affichera des informations sur le déroulement des tâches.
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.verbose('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        self.verbose('Setting window title.')
        self.setWindowTitle('Prediction App')

    """
    Gestion de la création de la modélisation.
    """
    def __compute_model(self):
        # model_th est un thread destiné à créer la modélisation.
        model_th = ModelingThread(data=self.data)
        # Les messages reçus par le signal "msg" seront traités par verbose pour les afficher.
        model_th.signals.msg.connect(lambda msg: self.verbose(*msg))
        # Une fois le travail fini, on rajoute un onglet contenant la vidéo du résultat.
        model_th.signals.finished.connect(lambda: self.__add_video_tab("Modeling", "outputs/brain_activation.mp4"))
        # On demande à threadpool de lancer le thread.
        self.threadpool.start(model_th)

    """
    Gestion de la création du graphique.
    """
    def __compute_graph(self):
        # graph_th est un thread destiné à créer la modélisation.
        graph_th = GraphThread(data=self.data)
        # Les messages reçus par le signal "msg" seront traités par verbose pour les afficher.
        graph_th.signals.msg.connect(lambda msg: self.verbose(*msg))
        # Une fois le travail fini, on rajoute un onglet contenant la vidéo du résultat.
        graph_th.signals.finished.connect(lambda: self.__add_video_tab("Graph", "outputs/camera.mp4"))
        # On demande à threadpool de lancer le thread.
        self.threadpool.start(graph_th)

    """
    Ajoute un onglet au tabwidget.
    """
    def __add_video_tab(self, name, path):
        self.main.addTab(VideoPlayer(os.path.abspath(path)), name)

    """
    Fait les traitements demandées (création du graphique et/ou de la modélisation).
    """
    def do_actions(self):
        # Si on a rien sélectionné, on ne fait rien, sinon on crée le dossier "outputs" s'il n'existe pas
        # puis on traite la demande.
        if not self.action['modeling'] and not self.action['graph']:
            self.verbose('Nothing to compute.')
        else:
            subprocess.call(["mkdir", "-p", "outputs"])

            if self.action['graph']:
                self.__compute_graph()
            if self.action['modeling']:
                self.__compute_model()

    """
    Permet de selectionner les traitements
    """
    def toggle_action(self, which):
        self.action[which] = not self.action[which]
        if self.action[which]:
            self.verbose('Predictions will be computed as a', which)
        else:
            self.verbose('Predictions will not be computed as a', which)

    """
    Permet d'écrire à la fois dans la console et dans la barre de statut.
    """
    def verbose(self, *args):
        self.statusBar.showMessage(' '.join(map(str, args)), 5000)
        print(*args)

    """
    Permet de récupérer le chemin du fichier de prédictions.
    """
    #TODO: A fusionner avec get_input_path()
    def get_path(self):
        # On recupère le chemin du fichier à l'aide d'une fenêtre montrant les fichiers csv présents sur le système.
        predictions_path, _ = QFileDialog.getOpenFileName(self, 'Open Prediction file', filter="CSV files (*.csv)")
        self.verbose('Selected file :', predictions_path)
        if predictions_path != "":
            self.data.set_predictions(predictions_path)

    """
    Permet de récupérer les chemins des fichiers d'entrée.
    """
    def get_input_path(self, filename, filetype):
        # Titre du chemin
        title = ' '.join(filename.split('_'))
        # Si on cherche un répertoire
        if filetype[-5:] == '(dir)':
            # On recupère le chemin du fichier à l'aide d'une fenêtre montrant les répertoires présents sur le système.
            path = QFileDialog.getExistingDirectory(
                self,
                "Open " + title + " path",
                "/home",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            self.verbose('Selected ' + title + ' path :', path)
        else:
            # On recupère le chemin du fichier à l'aide d'une fenêtre montrant les fichiers du bon type présents sur
            # le système.
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Open " + filename + " file",
                filter=filetype
            )
            self.verbose('Selected ' + title + ' path :', path)
        # Si l'utilisateur n'a pas annulé on note le chemin sinon on le retire s'il existait un chemin pour ce fichier.
        if path != "":
            self.paths[filename] = path
            return path
        elif filename in self.paths:
            del self.paths[filename]

    """
    Récupérer le widget principal.
    """
    def get_main(self):
        return self.main

    """
    Récupérer les chemins des fichiers de données
    """
    def get_data(self):
        return self.data

    """
    Lancer l'application
    """
    def __run(self):
        self.show()
        self.verbose('App started')
