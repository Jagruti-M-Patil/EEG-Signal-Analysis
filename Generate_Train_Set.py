from math import nan
import os
import random
import pandas as pd

import Parameters
from modules.Load_EEG_Data import getEdfDataAndLabels, ChannelsNotFoundError

edf_period_labels_file_path = os.path.join(Parameters.save_path, 'edf-file-period-labels.csv')
edf_period_labels_df = pd.read_csv(edf_period_labels_file_path)

train_preictal_data_fraction = 0.1
train_interictal_data_fraction = 0.1
train_data_column = []

files = edf_period_labels_df['File Name'].value_counts()

for file_name, count in files.items() :

	try :

		getEdfDataAndLabels(file_name)

		# If count greater than 1, means it has a preictal period
		if count > 1 :

			train_data_column.append(random.random() < train_preictal_data_fraction)

		else :

			train_data_column.append(random.random() < train_interictal_data_fraction)

	except ChannelsNotFoundError :

		print('Cannot find all channels in ' + file_name)
		train_data_column.append(nan)

	except FileNotFoundError :

		print('Cannot find file ' + file_name)
		train_data_column.append(nan)


files_df = pd.DataFrame(files)
files_df['Train'] = train_data_column

files_df.dropna(inplace=True)

# print(files_df)

save_file_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
files_df.to_csv(save_file_path, ',')