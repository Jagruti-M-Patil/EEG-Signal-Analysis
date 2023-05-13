import os
import mne

import numpy as np
import pandas as pd

import modules.Seizure_Period as Seizure_Period

import Parameters

edf_period_labels_file_path = os.path.join(Parameters.save_path, 'edf-file-period-labels.csv')
edf_period_labels_df = pd.read_csv(edf_period_labels_file_path)

class ChannelsNotFoundError(Exception) :

	def __init__(self, channels:list[str]) -> None:
		
		channels_not_found = set(Parameters.EEG_Channels).difference(channels)
		super().__init__('Channels not found - ' + str(channels_not_found))

def getEdfData(edf_file_name:str) -> mne.io.BaseRaw :

	rows = edf_period_labels_df.loc[edf_period_labels_df['File Name'] == edf_file_name]
	if rows.empty : raise FileNotFoundError('\"' + edf_file_name + '\" not in database.')
	
	case_id = list(rows['Case'])[0]

	edf_file_path = os.path.join(Parameters.EEG_dataset_path, case_id, edf_file_name)

	edf_data = mne.io.read_raw_edf(edf_file_path, verbose=False, include = Parameters.EEG_Channels)

	if set(edf_data.ch_names) != set(Parameters.EEG_Channels) : raise ChannelsNotFoundError(edf_data.ch_names)

	return edf_data

def getSignalLabels(edf_data:mne.io.BaseRaw, edf_file_name:str) -> np.ndarray :
	'''	Returns an array of length = no. of samples.
		Each element tells whether the sample was taken during a
		Preictal, Ictal or Interictal period '''
	
	rows = edf_period_labels_df.loc[edf_period_labels_df['File Name'] == edf_file_name]

	labels = np.zeros(edf_data.n_times, dtype=Seizure_Period.label)

	for row_no, row in rows.iterrows() :

		indices = np.logical_and(
			edf_data.times >= row['Period Start Time'] - row['File Start Time'],
			edf_data.times <= row['Period End Time'] - row['File Start Time']
		)

		labels[indices] = Seizure_Period.label(row['Period Label'])

	return labels

def getSignalData(edf_raw_data:mne.io.BaseRaw) -> np.ndarray :

	return edf_raw_data.get_data(picks=Parameters.EEG_Channels)

def getInputSignal(signal_data:np.ndarray, index:int) -> np.ndarray :

	index += 1

	if index < Parameters.window_len :

		ret_val = np.zeros((signal_data.shape[0], Parameters.window_len))

		ret_val[:, Parameters.window_len - index:] = signal_data[:, :index]

		return ret_val

	else :

		return signal_data[:, index - Parameters.window_len: index]

def generateInputSignalBatch(signal_data:np.ndarray, indices:list) -> np.ndarray :

	ret_val = np.zeros((len(indices), signal_data.shape[0], Parameters.window_len))

	for i, signal_index in enumerate(indices) :

		ret_val[i] = getInputSignal(signal_data, signal_index)

	return ret_val

