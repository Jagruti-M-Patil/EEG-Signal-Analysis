import os
import mne
import numpy as np
import tensorflow as tf
from sklearn.svm import SVC

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data

model_name = 'Approx_SVC_ARCoeff'

# Define the input shape
input_shape = tuple((2*2*len(Parameters.EEG_Channels),))

model = None
batch_size = 32

def generateModel() :

	global model

	# Define the model
	model = SVC()

	model.fit()

	pass

def ar_order(data):

	order = 2

	n_samples, n_channels = data.shape

	ar_features = np.zeros((n_samples,order * n_channels))

	for i in range(n_samples):
		for j in range(n_channels):

			# Autoregressive modeling using Yule-Walker equations
			ar_coeffs = np.polyfit(data[i, j:(order+j)], data[i, j+1:(order+j+1)], order-1)
			ar_features[i, (j*order):((j+1)*order)] = ar_coeffs
	
	return ar_coeffs 

def getInput(signal_data:np.ndarray, index:int) -> np.ndarray :

	input_signal = Load_EEG_Data.getInputSignal(signal_data, index)

	return np.apply_along_axis(ar_order,0,input_signal).flatten()

def trainEdf(edf_data:mne.io.base, output_data:np.ndarray, train_indices:list) -> float :

	edf_data.load_data(verbose=False)
	
	filtered_edf_data = edf_data.notch_filter(50, verbose=False)

	signal_data = Load_EEG_Data.getSignalData(filtered_edf_data)

	return trainByBatch(signal_data, output_data, train_indices)

def saveCheckpoint(file_name:str='checkpoint.ckpt') :

	path = os.path.join(Parameters.save_path, 'ML models', model_name, 'Train', file_name)

	model.save_weights(path)

	pass

def saveModel(file_name:str) -> None :

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	model.save(path)

	pass

def loadModel(file_name:str) :

	global model

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	model = tf.keras.models.load_model(path)

	pass

def predict(signal_input:np.ndarray) :

	return model.predict(signal_input)

def trainByBatch(signal_data, output_data, train_indices:np.ndarray) -> float :
    
	for step in range(train_indices.shape[0] // batch_size):

		batch_indices = train_indices[step * batch_size : (step + 1) * batch_size]

		batch_x = generateInputBatch(signal_data, batch_indices)
		batch_y = output_data[batch_indices]

		loss, acc = model.train_on_batch(batch_x, batch_y)

	return acc

def generateInputBatch(signal_data:np.ndarray, indices:list) -> np.ndarray :

	ret_val = np.zeros((batch_size, input_shape[0]))

	for i, signal_index in enumerate(indices) :

		ret_val[i] = getInput(signal_data, signal_index)

	return ret_val
