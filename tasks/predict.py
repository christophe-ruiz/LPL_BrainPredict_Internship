"""
    Author: Youssef Hmamouche
    Year: 2019
    Compute predictions based on pretrained models
"""

import os
import glob
import pandas as pd
import numpy as np
import joblib
import argparse
from ast import literal_eval
import sys

from PyQt5.QtCore import QObject
from tasks.signals import Signals

from sklearn.metrics import recall_score, precision_score, f1_score, average_precision_score


class Predict(QObject):
    def __init__(self, regions, type, pred_module_path, input_dir, lag=6):
        super(Predict, self).__init__()
        self.type = type
        self.lag = lag
        self.pred_module_path = pred_module_path
        self.input_dir = input_dir
        self.signals = Signals()

        # GET REGIONS NAMES FOR THEIR CODES
        brain_areas_desc = pd.read_csv("data/brain_areas.tsv", sep='\t', header=0)
        self.regions = []
        for num_region in regions:
            regions.append(brain_areas_desc.loc[brain_areas_desc["Code"] == num_region, "Name"].values[0])

        if self.pred_module_path[-1] == '/':
            self.pred_module_path = self.pred_module_path[:-1]

        out_dir = "%s/outputs/generated_time_series/" % self.input_dir

        # WRIGHT MULTIMODAL TIME SERIES TO CSV FILE
        all_data = pd.read_csv("%s/outputs/generated_time_series/all_features.csv" % self.input_dir, sep=';', header=0)
        columns = all_data.columns

        print("0")
        lagged_names = []
        for col in columns[1:]:
            lagged_names.extend([col + "_t%d" % p for p in range(self.lag, 2, -1)])

        all_data = pd.DataFrame(self.reorganize_data(all_data.values[:, 1:], lag=6, step=1), columns=lagged_names)

        """ load the best models for each regions """
        if self.type == 'h':
            conversation_type = 'HH'
        elif self.type == 'r':
            conversation_type = 'HR'
        else:
            print("Error in arguments, type of conversation missing, use -h for help!")
            exit(1)

        trained_models = glob.glob("%s/trained_models/*%s.pkl" % (self.pred_module_path, conversation_type))

        # dictionary of predictions: results
        preds = {}
        predictors_variables = {}
        nb_r = 1

        for region in regions:
            print(region, '\n', 18 * '-')
            predictors_data = pd.DataFrame()
            predictors_data.columns = []
            fname = ""
            for filename in trained_models:
                if region in filename:
                    fname = filename
                    break

            model_name = fname.split('/')[-1].split('_')[0]
            # print (model_name)
            model = joblib.load(fname)

            predictors = literal_eval(self.get_predictors_dict(model_name, region, self.type, self.pred_module_path))
            # print ("Predictors time series: ", predictors, "\n -------------")

            predictors_data = all_data.loc[:, predictors].values

            pred = model.predict(predictors_data)

            preds[region] = [0 for i in range(self.lag)] + pred.tolist()

            # Selected variables without lags
            predictors_variables[region] = self.get_features_from_lagged(predictors)
            # predictors_variables [region] = literal_eval (get_predictors (model_name, region, args. type, args.pred_module_path))
            # print (region, "\n", 18 * '-')
            print(int(100 * float(nb_r) / len(regions)))
            nb_r += 1
        preds_var = pd.DataFrame()

        for col in predictors_variables.keys():
            str_feat = predictors_variables[col].split(',')
            # print (str_feat)
            str_feat = ', '.join(map(str, str_feat))
            print(str_feat)
            preds_var[col] = [str_feat]

        # time index : fMRI recording frequency
        step = 1.205
        index = [step]
        for i in range(1, self.lag + len(pred)):
            index.append(index[i - 1] + step)

        pd.DataFrame(preds, index=index).to_csv("%s/outputs/predictions.csv" % self.input_dir, sep=';',
                                                index_label=["Time (s)"])
        preds_var.to_csv("%s/outputs/predictors.csv" % self.input_dir, sep=';', index=False)

    def reorganize_data (self, data_, lag = 6, step = 1):
        """
            step: ratio between frequencies of two time index (1.205 s)
            lag: lag
        """

        out_data = []

        # first point 0.6s correspont to the first BOLD acquisition
        lag0 = 1
        real_lag = lag - 2

        for i in range (lag, len (data_), step):
            row = []
            for j in range (data_. shape [1]):
                row = row + list (data_ [i - lag : i -  lag + real_lag, j]. flatten ()) #+ [np. sum (data_ [i - lag : i - lag + 3, j])]
                #row = row + [np. mean (data_ [i - lag : i -  lag + real_lag, j]), np. std (data_ [i - lag : i -  lag + real_lag, j])]
            out_data. append (row)

        return np. array (out_data)
    #---------------------------------------------------#
    def get_features_from_lagged (self, lagged_variables):
        features = set (['_'. join (a.split ('_')[0:-1]) for a in lagged_variables])
        return ','. join (map (str, list (features)))


    #---------------------------------------------------#
    def get_predictors (self, model_name, region, type, path):
        """
        model_name: name the PredictionModule model
        region: brain area
        type: interaction type (h (human-human) or r (human-robot))
        """
        model_params = pd. read_csv ("%s/results/PredictionModule/%s_H%s.tsv"%(path, model_name, type. upper ()), sep = '\t', header = 0)
        print (model_params. loc [model_params["region"] == "%s"%region]["predictors_dict"])
        predictors = model_params . loc [model_params["region"] == "%s"%region]["predictors_dict"]. iloc [0]

        return predictors

    #---------------------------------------------------#
    def get_predictors_dict (self, model_name, region, type, path):
        """
        model_name: name the PredictionModule model
        region: brain area
        type: interaction type (h (human-human) or r (human-robot))
        """
        model_params = pd. read_csv ("%s/results/PredictionModule/%s_H%s.tsv"%(path, model_name, type. upper ()), sep = '\t', header = 0)
        predictors = model_params . loc [model_params["region"] == "%s"%region]["selected_predictors"]. iloc [0]

        return predictors
