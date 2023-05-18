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
	'''	Loads data from edf file to a \'mne.io.RawEDF\' object.
		Does not preload the signal data. '''

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
	if rows.empty : raise FileNotFoundError('\"' + edf_file_name + '\" not in database.')

	labels = np.zeros(edf_data.n_times, dtype=Seizure_Period.label)

	for row_no, row in rows.iterrows() :

		indices = np.logical_and(
			edf_data.times >= row['Period Start Time'],
			edf_data.times < row['Period End Time']
		)

		labels[indices] = Seizure_Period.label(row['Period Label'])

	return labels

def getSignalData(edf_raw_data:mne.io.BaseRaw) -> np.ndarray :
	'''	Returns the signal data in a ndarray of the shape -
		(no of channels) x (no of samples)	'''

	return edf_raw_data.get_data(picks=Parameters.EEG_Channels)

def getInputSignal(index:int, signal_data:np.ndarray) -> np.ndarray :
	'''	Returns a window of signal data as an ndarray of the shape -
		(no of channels) x (no of samples in a window).
		out_array[:,-1] corresponds to the signal at time t[index],
		out_array[:, 0] corresponds to the signal at time t[index - window_len].
	'''

	index += 1

	ret_mat = np.zeros((len(Parameters.EEG_Channels), Parameters.window_len))
	ret_mat [:, max(0, Parameters.window_len - index):] = signal_data[:, max(0, index - Parameters.window_len): index]

	return ret_mat

def getTrainMask(edf_data:mne.io.BaseRaw, edf_file_name:str) :

	mask = np.zeros(edf_data.n_times, dtype=bool)

	rows = edf_period_labels_df.loc[edf_period_labels_df['File Name'] == edf_file_name]
	if rows.empty : raise FileNotFoundError('\"' + edf_file_name + '\" not in database.')

	last_interictal_row = pd.Series()

	for row_no, row in rows.iterrows() :

		indices = []

		if Seizure_Period.label(row['Period Label']) == Seizure_Period.label.Preictal :

			if last_interictal_row.empty :

				indices = np.logical_and(
					edf_data.times >= row['Period Start Time'],
					edf_data.times < row['Period End Time']
				)

			else :

				indices = np.logical_and(
					edf_data.times >= max(last_interictal_row['Period Start Time'], row['Period Start Time'] - 15 * 60),
					edf_data.times < row['Period End Time']
				)

			mask[indices] = True

		if Seizure_Period.label(row['Period Label']) == Seizure_Period.label.Interictal :

			last_interictal_row = row.copy()

		else :

			last_interictal_row = pd.Series()

	return mask

def getAnnotation(edf_file_name:str) :

	rows = edf_period_labels_df.loc[edf_period_labels_df['File Name'] == edf_file_name]
	if rows.empty : raise FileNotFoundError('\"' + edf_file_name + '\" not in database.')

	onset		= []
	duration	= []

	labels	= []

	for row_no, row in rows.iterrows() :

		labels.append(Seizure_Period.label(row['Period Label']).name)
		
		onset.append(row['Period Start Time'])
		duration.append(row['Period End Time'] - row['Period Start Time'])

		pass

	return mne.Annotations(onset, duration, labels)

