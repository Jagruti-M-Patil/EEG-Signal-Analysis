import os
import mne
import pickle
import numpy as np

from sklearn.svm import SVC
from typing import Literal
from tqdm import tqdm

import modules.Power_Spectral_Density as psd

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data

model = None

PROCESS_TYPE = Literal['test', 'train']

##############################################################################################################################

model_name = 'Spectral-SVM-Linear'
input_shape = (len(psd.bands.keys()) * len(Parameters.EEG_Channels),) # Keep channels as the last dimension

def generateModel() :

	global model

	# Define the model architecture
	model = SVC(kernel='linear', class_weight='balanced')

	pass

def generateModelInput(signal_data:np.ndarray) -> np.ndarray :
	'''	Generates an ndarray of the shape \'input_shape\',
		that is fed to the ML model. '''

	model_input = np.zeros(input_shape)

	# Perform any transforms here

	model_input = psd.compute_psd(signal_data).T.flatten()

	return model_input # Return array such that channel no is the last dimension

##############################################################################################################################

def saveModel(file_name:str='Model_Params.pickle') -> None :

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	with open(path, 'wb') as handle:

		pickle.dump(model.get_params(), handle, protocol=pickle.HIGHEST_PROTOCOL)

	pass

def loadModel(file_name:str='Model_Params.pickle') :

	global model

	path = os.path.join(Parameters.save_path, 'ML models', model_name, file_name)

	with open(path, 'rb') as handle:
		
		model.set_params(pickle.load(handle))

	pass

def predict(model_input:np.ndarray) :

	return model.predict(model_input)

def generateInputBatch(signal_data:np.ndarray, indices:list) -> np.ndarray :

	ret_val = np.zeros(indices.shape + input_shape)

	for i, signal_index in enumerate(indices) :

		ret_val[i] = generateModelInput(Load_EEG_Data.getInputSignal(signal_index, signal_data))

	return ret_val
