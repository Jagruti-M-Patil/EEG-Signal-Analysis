import os
import mne
import numpy as np
import tensorflow as tf
from typing import Literal
from tqdm import tqdm

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Auto_Regression as AR

model = None
batch_size = 32

PROCESS_TYPE = Literal['test', 'train']

##############################################################################################################################

model_name = 'AR_Dense'
input_shape = (AR.order, AR.order, len(Parameters.EEG_Channels)) # Keep channels as the last dimension

def generateModel() :

	global model

	# Define the model architecture
	model = tf.keras.Sequential(
		[
			tf.keras.layers.Input(shape=input_shape),
			tf.keras.layers.Flatten(),
			tf.keras.layers.Dense(units=64, activation='relu'),
			tf.keras.layers.Dense(units=32, activation='relu'),
			tf.keras.layers.Dense(units=1, activation='sigmoid')
		]
	)

	# Compile the model
	model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

	pass

def generateModelInput(signal_data:np.ndarray) -> np.ndarray :
	'''	Generates an ndarray of the shape \'input_shape\',
		that is fed to the ML model. '''

	model_input = np.zeros(input_shape)

	# Perform any transforms here

	model_input = np.apply_along_axis(AR.estimateARCoefficients, 1, signal_data)

	return model_input # Return array such that channel no is the last dimension

def processEDF(edf_data:mne.io.base, output_data:np.ndarray, indices:list, process:PROCESS_TYPE) -> tuple[float, float] :

	edf_data.load_data(verbose=False)

	# Perform EDF data preprocessing here

	filtered_edf_data = edf_data.notch_filter(50, verbose=False)

	signal_data = Load_EEG_Data.getSignalData(filtered_edf_data)

	if process == 'train' : func = model.train_on_batch
	elif process == 'test' : func = model.test_on_batch

	for step in tqdm(range(indices.shape[0] // batch_size)) :

		batch_indices = indices[step * batch_size : (step + 1) * batch_size]

		batch_x = generateInputBatch(signal_data, batch_indices)
		batch_y = output_data[batch_indices]

		loss, acc = func(batch_x, batch_y, reset_metrics=False)
	
	return loss, acc

##############################################################################################################################

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

def predict(model_input:np.ndarray) :

	return model.predict(model_input)

def generateInputBatch(signal_data:np.ndarray, indices:list) -> np.ndarray :

	ret_val = np.zeros((batch_size,) + input_shape)

	for i, signal_index in enumerate(indices) :

		ret_val[i] = generateModelInput(Load_EEG_Data.getInputSignal(signal_index, signal_data))

	return ret_val
