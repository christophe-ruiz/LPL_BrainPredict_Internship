from PyQt5.QtCore import QObject
from tasks.signals import Signals
import pandas as pd
import numpy as np
import os
import glob


class GenerateTimeSeries(QObject):

    def __init__(self, regions, openface_path, pred_module_path, input_dir, video_path, audio_input, language="fr"):
        super(GenerateTimeSeries, self).__init__()
        self.signals = Signals()
        self.video_path = video_path
        self.audio_input = audio_input
        self.openface_path = openface_path
        self.language = language
        self.pred_module_path = pred_module_path[:-1] if pred_module_path[-1] == '/' else pred_module_path
        self.input_dir = input_dir[:-1] if input_dir[-1] == '/' else input_dir
        self.out_dir = "%s/outputs/generated_time_series/" % self.input_dir
        # GET REGIONS NAMES FOR THEIR CODES
        self.brain_areas_desc = pd.read_csv("data/brain_areas.tsv", sep='\t', header=0)
        self.regions = []
        for num_region in regions:
            self.regions.append(
                self.brain_areas_desc
                    .loc[self.brain_areas_desc["Code"] == num_region, "Name"]
                    # .values[0]
            )

    def start(self):
        """ CREATE OUTPUT DIRECTORIES OF THE GENERATED TIME SERIES """
        for dirct in ["%s/outputs" % self.input_dir, self.out_dir,
                      "%s/outputs/generated_time_series/speech" % self.input_dir,
                      "%s/outputs/generated_time_series/video" % self.input_dir,
                      "%s/outputs/generated_time_series/eyetracking" % self.input_dir,
                      "%s/outputs/generated_time_series/emotions" % self.input_dir,
                      "%s/outputs/generated_time_series/energy" % self.input_dir,
                      "%s/outputs/generated_time_series/smiles" % self.input_dir
                      ]:
            if not os.path.exists(dirct):
                self.signals.msg.emit(("Creating directory: ", dirct))
                os.makedirs(dirct)

        """ GENERATE MULTIMODAL TIME SERIES FROM RAW SIGNALS """
        speech_left, speech = self.speech_features()
        self.signals.msg.emit(("Speech features created.",))
        video = self.facial_features(self.pred_module_path, self.input_dir, self.openface_path)
        self.signals.msg.emit(("Facial features created.",))
        # Extract other facial features: emotions, energy based features ...
        self.signals.msg.emit(("Creating extra features.",))
        eyetracking = self.extra_features("eyetracking")
        emotions = self.extra_features("emotions")
        energy = self.extra_features("energy")
        smiles = self.extra_features("smiles")
        self.signals.msg.emit(("Extra features created.",))

        """ CONCATENATE AND SAVE MULTIMODAL DATA """
        self.signals.msg.emit(("Concatenating data.",))
        all_data = np.concatenate((speech_left.values,
                                   speech.values[:, 1:],
                                   eyetracking.values[:, 1:],
                                   emotions.values[:, 1:],
                                   energy.values[:, 1:],
                                   smiles.values[:, 1:]
                                   ), axis=1)
        columns = list(speech_left.columns) +\
                  list(speech.columns[1:]) +\
                  list(eyetracking.columns[1:]) +\
                  list(emotions.columns[1:]) +\
                  list(energy.columns[1:]) +\
                  list(smiles.columns[1:])
        pd.DataFrame(all_data, columns=columns).to_csv(self.out_dir + "all_features.csv", sep=';', index=False)
        self.signals.finished.emit()

    def speech_features(self):
        """
        generate speech features from audio files
        pred_path: path of the PredictionModule module
        compute_features: logical, for computing the features or not (if they alreadu exists)
        out_dir: output directory
        """

        audio_output = self.out_dir + "speech"

        lang = None
        if self.language == "fr":
            lang = "fra"
        elif self.language == "eng":
            lang = "eng"

        os.system(
            "python %s/src/utils/SPPAS/sppas/bin/normalize.py -r %s/src/utils/SPPAS/resources/vocab/eng.vocab -I %s  -l %s -e .TextGrid --quiet" % (
                self.pred_module_path, self.pred_module_path, self.audio_input, lang)
        )
        os.system(
            "python %s/src/utils/SPPAS/sppas/bin/phonetize.py  -I %s -l %s -e .TextGrid" % (
                self.pred_module_path, self.audio_input, lang
            )
        )
        os.system(
            "python %s/src/utils/SPPAS/sppas/bin/alignment.py  -I %s -l %s -e .TextGrid --aligner basic" % (
                self.pred_module_path, self.audio_input, lang
            )
        )

        out = os.system(
            "python %s/src/generate_ts/speech_features.py %s %s/ -lg %s -n" % (
                self.pred_module_path, self.audio_input, audio_output, self.language
            )
        )
        out = os.system(
            "python %s/src/generate_ts/speech_features.py %s %s/ -l -lg %s -n" % (
                self.pred_module_path, self.audio_input, audio_output, self.language
            )
        )

        if self.out_dir[-1] != '/':
            self.out_dir += '/'
        speech = pd.read_pickle("%s/speech_features.pkl" % audio_output)
        speech_left = pd.read_pickle("%s/speech_features_left.pkl" % audio_output)
        return speech_left, speech

    def facial_features(self, pred_path, out_dir, openface_path):
        """ facial features  """

        video_output = self.out_dir + "video/"
        video_path = self.video_path
        print('video path before transofmration: ', video_path)

        energy_output = "%s/outputs/generated_time_series/video/" % out_dir

        if len(video_path) == 0:
            print("Error: there no input video!")
            exit(1)
        # else:
        #     video_path = video_path[0]

        video_name = video_path.split('/')[-1].split('.')[0]
        # openface_csv_file = "%s/outputs/generated_time_series/video/%/%.csv"%(out_dir,video_name)

        if out_dir[-1] != '/':
            out_dir += '/'

        os.system("python %s/src/generate_ts/facial_action_units.py %s %s -op %s" % (
            pred_path, video_path, video_output, openface_path))
        openface_features = glob.glob(video_output + "/" + video_path[:-4].split('/')[-1] + "/*.csv")[0]
        os.system("python %s/src/generate_ts/energy.py %s %s -faf %s -d" % (
            pred_path, video_path, energy_output, openface_features))

        video_features = glob.glob(video_output + "/*.pkl")
        video_feats = pd.read_pickle(video_features[0])
        facial_feats = pd.read_pickle(video_features[1])
        return pd.concat([video_feats, facial_feats], axis=1)

    def extra_features(self, type):
        """ eyetracking data """

        video_output = self.out_dir + "video"
        eyetracking_output = self.out_dir + type
        video_path = self.video_path
        if len(video_path) == 0:
            print("Error: there is no input video!")
            exit(1)
        # else:
        #     video_path = video_path[0]

        # print ("Processing eyetracking data")
        if self.out_dir[-1] != '/':
            self.out_dir += '/'

        openface_features = glob.glob(video_output + "/" + video_path[:-4].split('/')[-1] + "/*.csv")[0]

        if type == "eyetracking":
            gaze_coordinates_file = glob.glob("%s/inputs/eyetracking/*.pkl" % self.input_dir)[0]
            out = os.system("python %s/src/generate_ts/eyetracking.py %s %s -d -eye %s -faf %s -sv" % (
                self.pred_module_path, video_path, eyetracking_output, gaze_coordinates_file, openface_features))

        elif type == "emotions":
            emotion_module_path = self.pred_module_path + "/src/utils/face_classification"
            out = os.system(
                "python %s/src/generate_ts/generate_emotions_ts.py -d %s %s -fcp %s" % (
                    self.pred_module_path, video_path, eyetracking_output, emotion_module_path
                )
            )

        elif type == "energy":
            out = os.system(
                "python %s/src/generate_ts/energy.py %s %s -d -faf %s" % (
                    self.pred_module_path, video_path, eyetracking_output, openface_features
                )
            )

        elif type == "smiles":
            out = os.system(
                "python %s/src/generate_ts/dlib_smiles.py -d %s %s" % (
                    self.pred_module_path, video_path, eyetracking_output
                )
            )

        print("%s/*.pkl" % eyetracking_output)
        eyetracking_filename = glob.glob("%s/*.pkl" % eyetracking_output)[0]
        eyetracking = pd.read_pickle(eyetracking_filename)

        return eyetracking