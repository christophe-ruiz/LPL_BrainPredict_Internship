import string
import numpy as np
import seaborn as sns

from data import Data
from matplotlib import pyplot as plt
from celluloid import Camera


class Graph:
    def __init__(self, data=Data()):
        print('Creating figure...')
        fig = plt.figure(figsize=(32, 18))

        print('Retrieving data to plot')
        self.predictions = data.get_predictions()
        self.areas = data.get_areas()

        self.cam = Camera(fig)
        print('Camera initialized.')

        for line in range(1, len(self.predictions)):
            self.animate(line)
            print('Animated plots for timecode:', self.predictions.iloc[line].iat[0])

        print('Saving file...')
        animation = self.cam.animate(interval=1205)
        animation.save("./outputs/camera.mp4")
        print('File saved.')

    def animate(self, when):
        print('Fetching data...')
        data = self.predictions.iloc[:int(when + 1)]
        i = 0
        for which in self.predictions.columns[1:]:
            # Tableau d'entiers issus de 3 chaînes de caractères auxquelles on a enlevé les caratères de ponctuation
            # Ces chaînes de caractères sont extraites du fichier brain_areas.tsv par délimitation du caractère : ','
            colors = [int(str.strip(c, string.punctuation)) for c in str.split(self.areas["Color"][i])[:3]]
            # Les couleurs en hexadécimal : les caractères retournés par hex() sauf les deux premiers
            # formattés sur deux chifres.
            hex_colors = [hex(c)[2:].zfill(2) for c in colors]
            print('Colors calculated.')

            i = i + 1
            print('Adding plot number', i, 'to figure...')
            plt.subplot(6, 1, i)
            plt.tight_layout(1.5)
            plt.xlim(np.min(self.predictions)[0], np.max(self.predictions)[0])
            plt.ylim(0., 1.)
            plt.xlabel("Time (s)", fontsize=20)
            plt.ylabel("Value", fontsize=20)

            print('Drawing line...')
            p = sns.lineplot(x=data["Time (s)"], y=data[which], data=data, color="#" + ''.join(hex_colors))
            plt.setp(p.lines, linewidth=7)
            p.tick_params(labelsize=17)
        self.cam.snap()
        print('Image snapped.')
