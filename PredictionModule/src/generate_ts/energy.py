"""
	Author: Youssef Hmamouche
	Year: 2019
	Compute features about head movment energy, contractions (AUs), head ositions ..
"""

import sys, os, inspect, argparse, importlib
import numpy as np
import pandas as pd
#from sklearn.cluster import KMeans

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)

resampling_spec = importlib.util.spec_from_file_location("resampling", "%s/src/resampling.py"%maindir)
resampling = importlib.util.module_from_spec(resampling_spec)
resampling_spec.loader.exec_module(resampling)

#================================================#
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("video", help = "the path of the video to process.")
	parser.add_argument("out_dir", help = "the path where to store the results.")
	parser.add_argument("--demo",'-d', help = "If this script is using for demo.", action = "store_true")
	#parser.add_argument("--eyetracking",'-eye', help = "the path of the eyetracking file (for demo).")
	parser.add_argument("--facial_features",'-faf', help = "the path of the facial features file (csv file) (for demo).")
	args = parser.parse_args()


	if args. out_dir[-1] != '/':
	    args. out_dir += '/'
		
	# This for an independant utilization of the script (outisde the experiment videos)
	if args. demo:
	    openface_file = args. facial_features
	    conversation_name = "facial_features_energy"
	else:
		# subject number from video path
		subject = args. video.split ('/')[-2]
		conversation_name = args. video.split ('/')[-1]. split ('.')[0]
		openface_file = "time_series/%s/facial_features_ts/%s/%s.csv"%(subject, conversation_name, conversation_name)

	# Input directory and output file
	out_file = args. out_dir + conversation_name


	# check if file already processed
	if os.path.exists (out_file + '.pkl'):
		print (out_file)
		print ("Warning, file already processed")
		exit (1)

	# check if feature extraction (openface) has been processed
	if not os.path.exists (openface_file):
	    print ("Error, file %s does not exists"%openface_file)
	    exit (1)

	# compute the index of the index BOLD signal frequency
	physio_index = [0.6025]
	for i in range (1, 50):
		physio_index. append (1.205 + physio_index [i - 1])

	# read  openface file
	openface_data = pd. read_csv (openface_file, sep = ',', header = 0)

	# feature extraction
	video_index = openface_data. loc [:," timestamp"]. values[1:]
	contractions = pd.DataFrame ()
	contractions ["Time (s)"] = openface_data [" timestamp"]. values
	contractions ["mouth_AU"] = openface_data. loc [:,[" AU10_r", " AU12_r"," AU14_r"," AU15_r"," AU17_r"," AU20_r", " AU23_r", " AU25_r", " AU26_r"]]. sum (axis = 1)
	contractions["eyes_AU"] = openface_data. loc [:, [" AU01_r", " AU02_r", " AU04_r", " AU05_r", " AU06_r", " AU07_r", " AU09_r"]]. sum (axis = 1)
	contractions["total_AU"] = contractions ["mouth_AU"] + contractions["eyes_AU"]
	contractions["Happiness"] = openface_data [" AU06_r"] * openface_data[" AU12_r"]
	contractions["Sadness"] = openface_data [" AU01_r"] * openface_data[" AU04_r"] * openface_data[" AU15_r"]
	contractions["Surprise"] = openface_data [" AU01_r"] * openface_data[" AU02_r"] * openface_data[" AU05_r"] * openface_data[" AU26_r"]
	contractions["Fear"] = openface_data [" AU01_r"] * openface_data[" AU02_r"] * openface_data[" AU04_r"] * openface_data[" AU05_r"]\
	                        +  openface_data [" AU07_r"] * openface_data[" AU20_r"] * openface_data[" AU26_r"]
	contractions["Anger"] = openface_data [" AU04_r"] * openface_data[" AU05_r"] * openface_data[" AU07_r"] * openface_data[" AU23_r"]
	contractions["Disgust"] =  openface_data [" AU02_r"] * openface_data[" AU04_r"] * openface_data[" AU09_r"] * openface_data[" AU15_r"] * openface_data[" AU17_r"]
	contractions["Contempt"] = openface_data [" AU12_r"] * openface_data[" AU14_r"]
	head_translation = openface_data. loc [:, [" timestamp", " pose_Tx", " pose_Ty", " pose_Tz"]]
	head_rotation = openface_data. loc [:, [" timestamp", " pose_Rx", " pose_Ry"," pose_Rz"]]

	# resampling
	output_time_series = pd.DataFrame (resampling. resample_ts (contractions. values, physio_index, mode = "mean"), columns = contractions.columns)

	# nose positions
	positions = 	[" timestamp"]
	for i in range (28, 32):
	    positions = positions + [" x_%d"%i, " y_%d"%i]

	#labels = np. array (KMeans (n_clusters = 8). fit (openface_data. loc [:,positions]. values). labels_). reshape (-1,1)
	#head_positions = np. concatenate ((openface_data. loc [:, [" timestamp"]]. values, labels), axis = 1)

	# sum of speed over X, Y, and Z axis
	head_positions = openface_data. loc [:,[" pose_Tx", " pose_Ty", " pose_Tz"]]. diff (). abs (). sum (axis = 1)

	head_positions = np. concatenate ((openface_data. loc [:, [" timestamp"]]. values, head_positions. values. reshape (-1, 1)), axis = 1)

	head_positions = resampling. resample_ts (head_positions, physio_index, mode = "mean")
	head_translation_energy = resampling. resample_ts (head_translation. values, physio_index, mode = "energy")
	head_rotation_energy = resampling. resample_ts (head_rotation. values, physio_index, mode = "energy")

	# features concatenation
	output_time_series["head_rotation_energy"] = head_rotation_energy [:,1]
	output_time_series["head_translation_energy"] = head_translation_energy [:,1]
	output_time_series["head_positions"] = head_positions [:,1]

	# save data in pickle file
	output_time_series.to_pickle (out_file + ".pkl")
