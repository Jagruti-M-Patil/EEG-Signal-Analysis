import os
import random
import pandas as pd
from math import nan

import Parameters
from modules.Load_EEG_Data import getEdfData, ChannelsNotFoundError

train_preictal_data_fraction = 0.1
train_interictal_data_fraction = 0.1

edf_period_labels_file_path = os.path.join(Parameters.save_path, 'edf-file-period-labels.csv')
edf_period_labels_df = pd.read_csv(edf_period_labels_file_path)

files_series = edf_period_labels_df['File Name'].value_counts()

files_list = files_series.index.to_list()
# files_list = []

train_data_column = []
case_id = []

for file_name in files_list :

	count = files_series.loc[file_name]

	try :
		rows = edf_period_labels_df.loc[edf_period_labels_df['File Name'] == file_name]
		if rows.empty : raise FileNotFoundError('\"' + file_name + '\" not in database.')
		
		getEdfData(file_name)

		case_id.append(rows['Case'].to_list()[0])

		# If count greater than 1, means it has a preictal period
		if count > 1 :

			train_data_column.append(random.random() < train_preictal_data_fraction)

		else :

			train_data_column.append(random.random() < train_interictal_data_fraction)

	except ChannelsNotFoundError :

		print('Cannot find all channels in ' + file_name)
		train_data_column.append(nan)
		case_id.append(nan)

	except FileNotFoundError :

		print('Cannot find file ' + file_name)
		train_data_column.append(nan)
		case_id.append(nan)


files_df = pd.DataFrame(files_series[files_list])
files_df['Train'] = train_data_column
files_df['Case'] = case_id

files_df.dropna(inplace=True)

# print(files_df)

save_file_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
files_df.to_csv(save_file_path, ',')