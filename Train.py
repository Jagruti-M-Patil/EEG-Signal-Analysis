import os
import numpy as np
import pandas as pd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

import ML_models.CNN as ML_Model

train_files_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_path)

train_files_df = train_files_df.loc[train_files_df['Train']]
# train_files_df = train_files_df.loc[train_files_df['Case'] == 'chb01']

files_list = train_files_df.index.to_list()
# files_list = []

ML_Model.generateModel()

epochs = 1

for epoch in range(epochs) :

	print("Epochs completed {}/{}".format(epoch, epochs))
	
	num_files_to_train = 1

	try :

		for file_name in files_list :

			edf_data = Load_EEG_Data.getEdfData(file_name)

			labels = Load_EEG_Data.getSignalLabels(edf_data, file_name)

			scalar_output = np.zeros_like(labels, dtype=float)
			scalar_output[labels == Seizure_Period.label.Preictal] = 1.

			train_indices, = np.nonzero(Load_EEG_Data.getTrainMask(edf_data, file_name))

			loss, acc = ML_Model.processEDF(edf_data, scalar_output, train_indices, 'train')

			ML_Model.saveCheckpoint()

			num_files_to_train -= 1
			if not num_files_to_train : break

		print('Accuracy : ' + str(acc))

	except KeyboardInterrupt :

		break

ML_Model.saveModel()
