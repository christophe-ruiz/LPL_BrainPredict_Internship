import cv2
import math

from visbrain.objects import BrainObj, SceneObj


class Modelling:
    def __init__(self, app, data=None):
        # if not isinstance(data, Data):
        #     raise Exception()
        app.verbose('Fetching modelling data...')
        self.predictions = data.get_predictions()
        self.areas = data.get_areas()
        self.left = data.get_left()
        self.right = data.get_right()
        app.verbose('Options initialization...')
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fps = 30
        self.out = cv2.VideoWriter("./outputs/brain_activation.mp4", self.fourcc, self.fps, (1400, 1000))
        app.verbose('Building modelling')
        self.__modellize(app)
        app.verbose('Building complete')

    def __update_brain(self, app, active_parts, color_data):
        app.verbose('update running')
        # Contiendra la liste des parcellations de gauche à activer
        left_data = []
        # Contiendra la liste des couleurs des parcellations de gauche
        left_activated = []
        # Contiendra la liste des couleurs des parcellations de droite
        right_data = []
        # Contiendra la liste des parcellations de droite à activer
        right_activated = []

        # Creation de la modelisation du cerveau
        brains = list()
        for brain in range(6):
            brains.append(BrainObj('inflated', hemisphere='both', translucent=False))

        # Creation de la scene dans laquelle on disposera la modelisation
        sc = SceneObj(bgcolor='black', size=(1400, 1000))

        # Ajout du modele à la scene
        kw = dict(title_size=14., zoom=0.5)

        # Si il n'y a pas de parcellation à activer, on sort
        if len(active_parts) != 0 and len(color_data) != 0:
            # Pour chaque parcellation
            for i in range(len(active_parts)):
                label = active_parts[i]
                # Si le label fini par '_L', c'est une parcellation de gauche
                if "L" in label[-1]:
                    left_data.append(int(color_data[i]))
                    left_activated.append(label)
                # Sinon c'est une parcellation de droite
                else:
                    right_data.append(int(color_data[i]))
                    right_activated.append(label)
            # On regroupe les parcellations de droite d'un côté et celles de gauche de l'autre.
            if len(right_activated) != 0 and len(right_data) != 0:
                for brain in brains:
                    brain.parcellize(self.right, hemisphere='right', select=right_activated, data=right_data)
            if len(left_activated) != 0 and len(left_data) != 0:
                for brain in brains:
                    brain.parcellize(self.left, hemisphere='left', select=left_activated, data=left_data)
        # On ajoute les différentes vues du cerveau à la scène
        sc.add_to_subplot(brains[0], row=0, col=0, rotate='right', title='Right', **kw)
        sc.add_to_subplot(brains[1], col=1, rotate='left', title='Left', **kw)
        sc.add_to_subplot(brains[2], row=1, rotate='top', title='Top', **kw)
        sc.add_to_subplot(brains[3], row=1, col=1, rotate='bottom', title='Bottom', **kw)
        sc.add_to_subplot(brains[4], row=2, col=0, rotate='back', title='Back', **kw)
        sc.add_to_subplot(brains[5], row=2, col=1, rotate='front', title='Front', **kw)

        return cv2.cvtColor(sc.render(), cv2.COLOR_BGR2RGB)

    def __modellize(self, app):
        # Contient le temps en secondes pendants lequel une image s'affiche
        time = self.predictions.iloc[0, 0]
        # Image de cerveau vierge
        first_img = self.__update_brain(app, [], [])
        # On affiche cette image tant que les première activations ne sont pas arrivées
        for i in range(math.floor(30 * time)):
            self.out.write(first_img)
        # Pour chaque lignes du fichier predictions.csv
        for i in range(3): # len(self.predictions.iloc[:, 0])
            # Contiendra les parcellations à activer
            activated = []
            # Contiendra la couleur des parcellations à activer
            new_data = []
            # Pour chaque colonne (sauf la première, le temps) à chaque ligne (donc pour chaque parcellation)
            for j in range(1, 3):#len(self.predictions.iloc[i])):
                # Si cette parcellation est à activer (vaut 1.0 en réel soit 1 en entier)
                if int(self.predictions.iloc[i, j]) == 1:
                    # On parcourt les lignes du fichier brain_areas.tsv
                    for k in range(len(self.areas.iloc[:, 0])):
                        # Si le valeur de la colonne 'Name' de cette ligne est le même nom que la colonne à activer
                        if self.areas.iloc[k, 0] == self.predictions.columns[j]:
                            # On ajout le label aux parcellations à activer
                            activated.append(self.areas.iloc[k, 3])
                            # On ajoute la couleur aux parcellations à activer
                            # Le dernier élément du tableau de la dernière colonne de la ligne.
                            new_data.append(int(str.split(self.areas.iloc[k, 4])[4][:-1]))
                            break
            # Le temps de début d'activation est récupéré
            time = self.predictions.iloc[i, 0]
            # Le temps de fin est récupéré
            time_plus = self.predictions.iloc[i + 1, 0] if i + 1 < len(self.predictions.iloc[:, 0]) else 65
            # Le delta du temps d'affichage est calculé
            delta = time_plus - time
            # L'image à afficher est récupérée
            img = self.__update_brain(app, activated, new_data)
            # On affiche l'image pendant delta secondes
            for j in range(math.floor(30 * delta)):
                self.out.write(img)

        self.out.release()
        cv2.destroyAllWindows()
