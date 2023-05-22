import os
import numpy as np
import pandas as pd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

import ML_models.Spectral_SVM_Linear as ML_Model

train_files_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_path)

train_files_df = train_files_df.loc[train_files_df['Train']]
# train_files_df = train_files_df.loc[train_files_df['Case'] == 'chb01']

# files_list = train_files_df['File Name'].to_list()
files_list = ['chb01_03.edf']

ML_Model.generateModel()

# Get Train Dataset Size
num_train_data = 0

for file_name in files_list :

	edf_data = Load_EEG_Data.getEdfData(file_name)

	num_train_data += np.count_nonzero(Load_EEG_Data.getTrainMask(edf_data, file_name))

print('Train Set : ', num_train_data)

try : 

	print('Creating Train Set...')

	x_batch = np.zeros((num_train_data,) + ML_Model.input_shape)
	y_batch = np.zeros(num_train_data)

	k = 0

	for file_name in files_list :

		edf_data = Load_EEG_Data.getEdfData(file_name)

		signal_data = Load_EEG_Data.getSignalData(edf_data)
		labels = Load_EEG_Data.getSignalLabels(edf_data, file_name)

		scalar_output = np.zeros_like(labels, dtype=float)
		scalar_output[labels == Seizure_Period.label.Preictal] = 1.

		train_indices, = np.nonzero(Load_EEG_Data.getTrainMask(edf_data, file_name))
		np.random.shuffle(train_indices)

		num = train_indices.shape[0]
		x_batch[k:k+num, ...] = ML_Model.generateInputBatch(signal_data, train_indices)
		y_batch[k:k+num] = scalar_output[train_indices]

		k += num

	print('Training...')

	ML_Model.model.fit(x_batch, y_batch)

	print('Saving model params...')
	ML_Model.saveModel()

except KeyboardInterrupt :

	print('Saving model params...')
	ML_Model.saveModel()

except np.core._exceptions._ArrayMemoryError :

	raise ValueError('Too huge dataset!!')

