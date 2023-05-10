import os, warnings
import numpy as np
import pandas as pd

from tqdm import tqdm

import mne

import Parameters

labels_file_path = os.path.join(Parameters.save_path, 'signal-labels.csv')
edf_file_labels = pd.read_csv(labels_file_path, sep=',')

time_array_save_dir_path = os.path.join(Parameters.save_path, 'Time Arrays')
npy_array_save_dir_path = os.path.join(Parameters.save_path, 'EEG Signal Arrays')

t_array_file = []
npy_signal_file = []

rem_rows = []

for file_count, row in tqdm(edf_file_labels.iterrows(), total=edf_file_labels.shape[0], desc='Converting EDF to npy') :
    
	case_id = row['case']

	edf_file_path = os.path.join(Parameters.EEG_dataset_path, case_id, row['f_name'])

	try :
	
		with warnings.catch_warnings() :

			warnings.simplefilter('ignore')
			edf_file = mne.io.read_raw_edf(edf_file_path, verbose=False)

		t_start, t_end = row['t_start'] - row['f_start_t'], row['t_end'] - row['f_start_t']

		EEG_signal_array, time_array = edf_file.get_data(tmin=t_start, tmax=t_end, return_times=True)
		time_array += row['f_start_t']

		np.save(os.path.join(time_array_save_dir_path, str(file_count)), time_array)
		t_array_file.append(str(file_count) + '.npy')

		channel_indices = [row[str(i)] for i in range(len(Parameters.EEG_Channels))]
		EEG_signal_array = EEG_signal_array[channel_indices]

		np.save(os.path.join(npy_array_save_dir_path, str(file_count)), EEG_signal_array)
		npy_signal_file.append(str(file_count) + '.npy')

	except FileNotFoundError :

		t_array_file.append(np.nan)
		npy_signal_file.append(np.nan)

# print(t_array_file)
# print(npy_signal_file)

edf_file_labels.drop(columns=[str(i) for i in range(len(Parameters.EEG_Channels))], inplace=True)

edf_file_labels['t_array_f'] = t_array_file
edf_file_labels['signal_f'] = npy_signal_file

edf_file_labels.dropna(inplace=True)

npy_labels_file_path = os.path.join(Parameters.save_path, 'npy-labels.csv')
edf_file_labels.to_csv(npy_labels_file_path)
