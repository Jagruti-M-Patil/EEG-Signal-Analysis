import os
import mne
import numpy as np
import tensorflow as tf
from tqdm import tqdm

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data

model_name = 'CNN-1D'

# Define the input shape
input_shape = (len(Parameters.EEG_Channels), Parameters.window_len)

model = None
batch_size = 32

def generateModel() :

	global model

	# Define the model architecture
	model = tf.keras.Sequential(
		[
			tf.keras.layers.Conv1D(32, kernel_size=3, activation="relu", input_shape=input_shape),
			tf.keras.layers.MaxPooling1D(pool_size=2),
			tf.keras.layers.Flatten(),
			tf.keras.layers.Dense(64, activation="relu"),
			tf.keras.layers.Dense(1, activation="sigmoid"),
		]
	)

	# Compile the model
	model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

	pass

def getInput(signal_data:np.ndarray, index:int) -> np.ndarray :

	input_signal = Load_EEG_Data.getInputSignal(signal_data, index)

	return input_signal

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
    
	for step in tqdm(range(train_indices.shape[0] // batch_size)):

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
