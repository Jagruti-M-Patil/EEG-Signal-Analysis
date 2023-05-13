import os
import numpy as np
import pandas as pd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

import ML_models.CNN as ML_Model

train_files_db_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_db_path)

ML_Model.generateModel()

batch_size = 32
epochs = 1

for epoch in range(epochs):

	print("Epochs completed {}/{}".format(epoch, epochs))

	try :

		for file_no, row in train_files_df.loc[train_files_df['Train']].iterrows() :

			edf_data = Load_EEG_Data.getEdfData(row['File Name'])

			labels = Load_EEG_Data.getSignalLabels(edf_data, row['File Name'])

			scalar_output = np.zeros_like(labels, dtype=float)
			scalar_output[labels == Seizure_Period.label.Preictal] = 1.

			train_indices, = np.nonzero(labels != Seizure_Period.label.Ictal)

			ML_Model.trainEdf(edf_data, scalar_output, train_indices)

		ML_Model.saveCheckpoint()

	except KeyboardInterrupt :

		pass

ML_Model.saveModel('Model')
