import os
import numpy as np
import pandas as pd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

import ML_models.CNN as ML_Model

train_files_db_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_db_path)

# train_files = train_files_df.loc[train_files_df['Train'] == False]['File Name'].tolist()
train_files = ['chb01_03.edf']

ML_Model.loadModel()

try :

	for file_name in train_files :

		edf_data = Load_EEG_Data.getEdfData(file_name)

		labels = Load_EEG_Data.getSignalLabels(edf_data, file_name)

		scalar_output = np.zeros_like(labels, dtype=float)
		scalar_output[labels == Seizure_Period.label.Preictal] = 1.

		test_indices, = np.nonzero(labels != Seizure_Period.label.Ictal)

		loss, acc = ML_Model.testEdf(edf_data, scalar_output, test_indices)

		print('Accuracy : ' + str(acc))

except KeyboardInterrupt :

	pass

try :
	
	print('Accuracy : ' + str(acc))

except NameError :

	print('Did not finish evaluation on any edf files')
