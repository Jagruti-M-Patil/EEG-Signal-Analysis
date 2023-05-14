import os
import numpy as np
import pandas as pd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

import ML_models.AR_Dense as ML_Model

train_files_db_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_db_path)

train_files_df = train_files_df.loc[train_files_df['Train']]
# train_files_df = train_files_df.loc[train_files_df['Case'] == 'chb01']

ML_Model.generateModel()

epochs = 1

for epoch in range(epochs) :

	print("Epochs completed {}/{}".format(epoch, epochs))

	try :

		num_files_to_train = 1

		for file_no, row in train_files_df.iterrows() :

			edf_data = Load_EEG_Data.getEdfData(row['File Name'])

			labels = Load_EEG_Data.getSignalLabels(edf_data, row['File Name'])

			scalar_output = np.zeros_like(labels, dtype=float)
			scalar_output[labels == Seizure_Period.label.Preictal] = 1.

			train_indices, = np.nonzero(Load_EEG_Data.getTrainMask(edf_data, row['File Name']))

			loss, acc = ML_Model.trainEdf(edf_data, scalar_output, train_indices)

			ML_Model.saveCheckpoint()

			num_files_to_train -= 1
			if not num_files_to_train : break

		print('Accuracy : ' + str(acc))

	except KeyboardInterrupt :

		break

ML_Model.saveModel()
