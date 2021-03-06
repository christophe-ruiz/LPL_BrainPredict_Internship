import string
import numpy as np
import seaborn as sns

from PyQt5.QtCore import QObject
from matplotlib import pyplot as plt
from celluloid import Camera
from tasks.signals import Signals


class Graph(QObject):
    def __init__(self, data=None):
        super().__init__()
        self.output_path = "outputs/camera.mp4"
        self.signals = Signals()
        self.signals.msg.emit(('Graph initialization...',))
        fig = plt.figure(figsize=(32, 18))

        self.predictions = data.get_predictions()
        self.areas = data.get_areas()

        self.cam = Camera(fig)

    def start(self):
        for line in range(1, len(self.predictions)):
            self.animate(line)
            self.signals.msg.emit(('Animated plots for timestamp:', self.predictions.iloc[line].iat[0]))

        self.signals.msg.emit(('Saving graph...',))
        animation = self.cam.animate(interval=1205)
        animation.save(self.output_path)
        self.signals.msg.emit(('Graph saved.',))
        self.signals.finished.emit()

    def animate(self, when):
        self.signals.msg.emit(('Computing image...',))
        data = self.predictions.iloc[:int(when + 1)]
        i = 0
        for which in self.predictions.columns[1:]:
            # Tableau d'entiers issus de 3 chaînes de caractères auxquelles on a enlevé les caratères de ponctuation
            # Ces chaînes de caractères sont extraites du fichier brain_areas.tsv par délimitation du caractère : ','
            colors = [int(str.strip(c, string.punctuation)) for c in str.split(self.areas["Color"][i])[:3]]
            # Les couleurs en hexadécimal : les caractères retournés par hex() sauf les deux premiers
            # formattés sur deux chifres.
            hex_colors = [hex(c)[2:].zfill(2) for c in colors]

            i = i + 1

            plt.subplot(6, 1, i)
            plt.tight_layout(1.5)
            plt.xlim(np.min(self.predictions)[0], np.max(self.predictions)[0])
            plt.ylim(0., 1.)
            plt.xlabel("Time (s)", fontsize=20)
            plt.ylabel("Value", fontsize=20)

            self.signals.msg.emit(('Drawing line...',))
            p = sns.lineplot(x=data["Time (s)"], y=data[which], data=data, color="#" + ''.join(hex_colors))
            plt.setp(p.lines, linewidth=7)
            p.tick_params(labelsize=17)
        self.cam.snap()
        self.signals.msg.emit(('Image snapped.',))
