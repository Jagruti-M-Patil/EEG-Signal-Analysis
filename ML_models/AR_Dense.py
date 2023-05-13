import os
import mne
import numpy as np
import tensorflow as tf
from scipy.linalg import toeplitz, lstsq
from scipy.signal import correlate

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data

model_name = 'AR-Dense'

# Define the input shape
ar_order = 2
input_shape = (len(Parameters.EEG_Channels), ar_order)

model = None
batch_size = 32

def generateModel() :

	global model

	# Define the model architecture
	model = tf.keras.models.Sequential([
		tf.keras.layers.Input(shape=input_shape),
		tf.keras.layers.Dense(units=128, activation='relu'),
		tf.keras.layers.Dense(units=64, activation='relu'),
		tf.keras.layers.Dense(units=32, activation='relu'),
		tf.keras.layers.Dense(units=1, activation='sigmoid')
	])

	# Compile the model
	model.compile(
		optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
		loss='mean_squared_error',
		metrics=['mae']
	)
	
	pass

def estimate_ar_coefficients(input_signal):
    
	autocorr = np.correlate(input_signal, input_signal, mode='full') # 2 * window_len - 1

	r = autocorr[(Parameters.window_len-1) : (Parameters.window_len-1) + (ar_order+1)] # ar_order + 1

	r_matrix = toeplitz(r[:-1]) # ar_order x ar_order

	ar_coeffs = lstsq(r_matrix, r[1:])[0]

	return ar_coeffs

def getInput(signal_data:np.ndarray, index:int) -> np.ndarray :

	input_signal = Load_EEG_Data.getInputSignal(signal_data, index) # no_channels x no_samples

	ar_input = np.apply_along_axis(estimate_ar_coefficients, 1, input_signal)

	return ar_input

def trainEdf(edf_data:mne.io.base, output_data:np.ndarray, train_indices:list) -> tuple[float, float] :

	edf_data.load_data(verbose=False)

	filtered_edf_data = edf_data.notch_filter(50, verbose=False)

	signal_data = Load_EEG_Data.getSignalData(filtered_edf_data)

	return trainByBatch(signal_data, output_data, train_indices)

def testEdf(edf_data:mne.io.base, output_data:np.ndarray, test_indices:list) -> tuple[float, float] :

	edf_data.load_data(verbose=False)

	filtered_edf_data = edf_data.notch_filter(50, verbose=False)

	signal_data = Load_EEG_Data.getSignalData(filtered_edf_data)

	return testByBatch(signal_data, output_data, test_indices)

def saveCheckpoint(file_name:str='checkpoint.ckpt') :

	path = os.path.join(Parameters.save_path, 'ML models', model_name, 'Train', file_name)

	model.save_weights(path)

	pass

def saveModel(file_name:str='Model') -> None :

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	model.save(path)

	pass

def loadModel(file_name:str='Model') :

	global model

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	model = tf.keras.models.load_model(path)

	pass

def predict(signal_input:np.ndarray) :

	return model.predict(signal_input)

def trainByBatch(signal_data, output_data, train_indices:np.ndarray) -> tuple[float, float] :
    
	for step in range(train_indices.shape[0] // batch_size):

		batch_indices = train_indices[step * batch_size : (step + 1) * batch_size]

		batch_x = generateInputBatch(signal_data, batch_indices)
		batch_y = output_data[batch_indices]

		loss, acc = model.train_on_batch(batch_x, batch_y, reset_metrics=False)

	return loss, acc

def testByBatch(signal_data, output_data, test_indices:np.ndarray) -> tuple[float, float] :
    
	for step in range(test_indices.shape[0] // batch_size):

		batch_indices = test_indices[step * batch_size : (step + 1) * batch_size]

		batch_x = generateInputBatch(signal_data, batch_indices)
		batch_y = output_data[batch_indices]

		loss, acc = model.test_on_batch(batch_x, batch_y, reset_metrics=False)

		if (batch_y == 1).any() : print('Accuracy : ' + str(acc))
	
	return loss, acc

def generateInputBatch(signal_data:np.ndarray, indices:list) -> np.ndarray :

	ret_val = np.zeros((batch_size,) + input_shape)

	for i, signal_index in enumerate(indices) :

		ret_val[i] = getInput(signal_data, signal_index)

	return ret_val
