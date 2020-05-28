#import scipy.io as sio
import pandas as pd
import numpy as np
from glob import glob
import os, sys

import argparse
from mat4py import loadmat
from skimage import filters
#import matplotlib.pyplot as plt
from sklearn.preprocessing import KBinsDiscretizer
#from sklearn.cluster import KMeans
from sklearn import preprocessing


def sigmoid (x):
    e = np.exp(1)
    y = 1/(1+e**(-x))
    return y

#====================================#
def smoothing (data, alpha = 0.7):
    data_s = [0 for i in range (len (data))]
    data_s [0] = data [0]
    #data_s [1] = data [1]
    for i in range (1, len (data)):
    	data_s[i] = alpha * data[i] + (1 - alpha) * data[i - 1]
        #data_s[i] = 0.5 * data[i] + 0.3 * data[i - 1] + 0.2 * data[i - 2]
    	#data_s[i] = data[i] - data[i - 1]
    return np. array (data_s)
#-----------------------------------------------------------------------------
# Plot dataframe
def plot_df (df, labels, figsize=(12,9), y_lim = [0,1.2]):
	fig = plt.figure(figsize = figsize)

	plt.title('Title!', color='black')
	df. plot (y=labels, sharex=True, subplots=True, xticks = df.index, fontsize = 7, grid=False, legend= False, ax=fig.gca())

	ld = fig.legend(labels = labels,
	       loc='upper right',   # Position of legend
	       prop={'size':6},
	       ncol=1,
	       fontsize = 'small')

	fig.text (0.5, 0.12, 'Time (s)', ha='center')
	fig.text (0.07, 0.5, 'Series', va='center', rotation='vertical')
	plt. show ()


#============================================================
def normalize_vect (x):
	max = np.max (x)
	min = np.min (x)

	if min < max:
		for i in range (len (x)):
			x[i]= (x[i] - min) / (max - min)

#============================================================
def get_sliding_windows (n, size = 10):
	winds = []
	for j in range (n + 1 - size):
		winds. append (range (j, j + size))

	return winds

#===========================================================
def discretize_vect (x, threshold):
	result = []
	for i in range (len (x)):
		if x[i] >= threshold:
			result. append ([1])
		else:
			result. append ([0])

	return result
#============================================================
def discretize_vect_sliding (x, win_size = 10):
	mat = []
	winds = get_sliding_windows (len (x), 10)

	for i in range (len (x)):
		values_in_windows = []
		for j in range (len (winds)):
			if i in winds[j]:
				indice_i = winds[j]. index (i)
				row = [x[k] for k in winds[j]]
				normalize_vect (row)

				if row [indice_i] > 0.5:
					values_in_windows. append (1)
				else:
					values_in_windows. append (0)

		# count the number of 1 in each moving window
		if (float (np. sum (values_in_windows)) / len (values_in_windows) > 0.5):
			mat. append (1.0)
		else:
			mat. append (0.0)
	return mat

#======================================================

def nearestPoint(vect, value):
    dist = abs(value - vect[0])
    pos = 0

    for i in range(1, len(vect)):
        if abs(value - vect[i]) < dist and value >= vect[i]:
            dist = abs(value - vect[i])
            pos = i

    return pos

#======================================================

def add_duration(df):
    duration = []

    for i in range(df.shape[0] - 1):
        '''if i == (df.shape[0] - 1):
            duration.append([df.iloc[i, 3] / 1000.0, df.iloc[i, 3] / 1000.0, 0])
        else:'''
        duration.append ([df.iloc[i, 3] / 1000.0, df.iloc[i + 1, 3] / 1000.0, df.iloc[i + 1, 3] / 1000.0 - df.iloc[i, 3] / 1000.0])

    df = pd.concat([df, pd.DataFrame(duration, columns=['begin', 'end', 'Interval'])], axis=1)

    return df

#======================================================

def convers_to_df (data, colnames, index, begin, end, type_conv, num_conv, concat):

	index_normalized = index[begin:end]
	start_pt = index_normalized [0]

	for j in range(0, end - begin):
	   index_normalized[j] -= start_pt

	convers_data = pd.DataFrame ()
	convers_data ["Time (s)"] = index_normalized

	convers_data_discr = pd.DataFrame ()
	convers_data_discr ["Time (s)"] = index_normalized

	for i in range (len (colnames)):
		convers_data. loc [:, colnames [i]] = data [begin : end, i]

	filename = "time_series/" + subject + "/physio_ts/convers-" + testBlock + "_" + type_conv + "_" + "%03d"%num_conv + ".pkl"
	filename_discr = "time_series/" + subject + "/discretized_physio_ts/convers-" + testBlock + "_" + type_conv + "_" + "%03d"%num_conv + ".pkl"

	if os.path.exists (filename) and os.path.exists (filename_discr) and concat:
		existed_data = pd. read_pickle (filename). iloc[:,1:]
		convers_data = pd. concat ([convers_data, existed_data], axis = 1)

	convers_data.to_pickle (filename)

#======================================================

if __name__ == '__main__':

    parser = argparse. ArgumentParser ()
    parser. add_argument ("--concat", "-ct", help = "remove previous files", action="store_true")
    args = parser.parse_args()

    mat_data = loadmat ("data/physio_data/ROIdata/resultsYH28022020.mat")

    index = [0]
    for i in range (1, 4 * 385):
        index. append (1.205 + index [i - 1])


    """ store the discretization parameters """
    f= open("disc_params.txt","w+")
    f. write ("Oslo discretization")

    # loop over subjects
    for s in range (25):
        subject = "sub-%02d"%(s + 1)
        print (subject)

        # Create folders if not exist
        for fname in ["physio_ts", "discretized_physio_ts"]:
        	if not os.path.exists ("time_series/%s/%s"%(subject, fname)):
        	    os.makedirs("time_series/%s/%s"%(subject, fname))

        nb_regions =  len (mat_data ["results"][s]["roi"])

        bol_signal = pd. DataFrame ()
        bold_signal_discretized = pd. DataFrame ()

        # loop over regions
        for r in range (nb_regions):
            region_name = mat_data ["results"][s]["roi"][r]['name']
            sessions =  mat_data ["results"][s]["roi"][r]['sess']

            # loop over sessions
            for i in range (4):
            	norm = np. array (sessions [i][:]). flatten ()

            	# Smoothing
            	norm = smoothing (norm, alpha = 0.5)
                # Normalization
            	normalize_vect (norm)

            	if i == 0:
            		region_data = np. array (norm)
            	else:
            		region_data = np. concatenate ((region_data, np. array (norm)), axis = 0)

            bol_signal [region_name] = region_data. flatten ()

        if bol_signal. shape[0] == 0:
            print ()
            continue

        colnames = bol_signal. columns
        bol_signal = bol_signal. values

        testBlocks = ["TestBlocks" + str (i + 1) for i in range (4)]

        #--------------------------------------------------------#
        indice_block = 0
        for testBlock in testBlocks:
            logfile = glob ("data/physio_data/logfiles/*" + subject + "_task-convers-" + testBlock + "*")
            if len (logfile) == 0:
                print ("Some logfiles do not exist for subject %s"%subject)
                continue
            else:
            	logfile = logfile [0]

            df = pd.read_csv (logfile, sep='\t', header=0)
            df = df [['condition', 'image', 'duration', 'ONSETS_MS']]

            df = add_duration (df)

            hh_convers = df [df.condition.str.contains("CONV1")] [['condition', 'begin', 'end']]
            hr_convers = df [df.condition.str.contains("CONV2")] [['condition', 'begin', 'end']]

            nb_hh_convers = hh_convers. shape [0]
            nb_hr_convers = hr_convers. shape [0]

            hh = 1
            hr = 2

            for i in range(nb_hh_convers):
                begin = nearestPoint (index, hh_convers.values[i][1]) + (385 * indice_block)
                end = nearestPoint (index, hh_convers.values[i][2]) + (385 * indice_block)  + 2 # add two observatiosn after the end of the conversation
                convers_to_df (bol_signal, colnames, index, begin, end, "CONV1", hh, args. concat)
                hh += 2

            for i in range(nb_hr_convers):
                begin = nearestPoint (index, hr_convers.values[i][1]) + (385 * indice_block)
                end = nearestPoint (index, hr_convers.values[i][2]) + (385 * indice_block) + 2 # add two observatiosn after the end of the conversation
                convers_to_df (bol_signal, colnames, index, begin, end, "CONV2", hr, args. concat)
                hr += 2
            indice_block += 1
    f. close ()
