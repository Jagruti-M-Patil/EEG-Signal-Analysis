# Created by Souritra Garai & Jagruti Patil, 2023
# This script sorts edf files into preictal / interictal class
# and Test / Train set after reading the 'chbXX-summary.txt' file
# Check the '__main__' part

import os
import random
import pandas as pd

preictal_period = 15 * 60 # seconds

columns = ['Case', 'Filename', 'Set', 'Class', 'Seizure Start', 'Crop Start', 'Crop End']

df = pd.DataFrame(columns=columns)

def getSummaryFilePath(patient_id:str, eeg_data_path) -> str :

	summary_file_name = patient_id + '-summary.txt'

	return os.path.join(eeg_data_path, patient_id, summary_file_name)

class UnexpectedFieldError(Exception) :

	def __init__(self, expected_value:str, line_no:int, last_line:str) -> None:
		
		super().__init__(
			'Expected \'' + expected_value +
			'\' at line no ' + str(line_no) + '.\n' +
			'Last line read was \'' +
			last_line + '\''
		)

	pass

def readField(line:str, field_name:str, line_no:int, last_line:str) -> str :

	line = line.strip() # Strip the starting and ending whitespace characters in the line

	words = line.split(': ') # Splits the line into segments separated by ': ' (There is a space after semi colon)

	if words[0].strip() != field_name :

		raise UnexpectedFieldError(field_name, line_no, last_line)
	
	else :
		
		return words[1].strip()

def readSummaryFile(summary_file_name_path:str, patient_id:str) :

	summary_file = open(summary_file_name_path, 'r')

	label_dict = dict()

	for field in columns : label_dict[field] = []

	# Read first line
	line = summary_file.readline()
	line_no = 1
	last_line = ''

	while line :

		try :

			edf_file_name = readField(line, 'File Name', line_no, last_line)		

		except UnexpectedFieldError :
			# If the line does not start with 'File Name', it is not a file description segment
			# So skip the present iteration and move to reading the next line

			# read next line
			last_line = line
			line = summary_file.readline() 
			line_no += 1

			continue

		# read next line
		last_line = line
		line = summary_file.readline() 
		line_no += 1

		start_time = readField(line, 'File Start Time', line_no, last_line)

		# read next line
		last_line = line
		line = summary_file.readline() 
		line_no += 1

		end_time = readField(line, 'File End Time', line_no, last_line)

		# read next line
		last_line = line
		line = summary_file.readline() 
		line_no += 1

		num_seizures = int(readField(line, 'Number of Seizures in File', line_no, last_line))

		if num_seizures == 0 :

			# Fill data into dictionary
			label_dict['Case'].append(patient_id)
			label_dict['Filename'].append(edf_file_name)
			label_dict['Class'].append('Interictal')
			label_dict['Seizure Start'].append(0)
			label_dict['Crop Start'].append(0)
			label_dict['Crop End'].append(preictal_period)

		# print(edf_file_name, start_time, end_time, num_seizures)

		while num_seizures != 0 :

			# read next line
			last_line = line
			line = summary_file.readline() 
			line_no += 1

			seizures_start_time = int(readField(line, 'Seizure Start Time', line_no, last_line).split()[0])

			# read next line
			last_line = line
			line = summary_file.readline() 
			line_no += 1

			seizures_end_time = int(readField(line, 'Seizure End Time', line_no, last_line).split()[0])

			# num_seizures -= 1
			num_seizures = 0 # In case edf file contains more than 1 seizure, only the first seizure data is used
			
			# print(seizures_start_time, seizures_end_time)

			if seizures_start_time > preictal_period :
				
				# Fill data into dictionary
				label_dict['Case'].append(patient_id)
				label_dict['Filename'].append(edf_file_name)
				label_dict['Class'].append('Preictal')
				label_dict['Seizure Start'].append(seizures_start_time)
				label_dict['Crop Start'].append(seizures_start_time - preictal_period)
				label_dict['Crop End'].append(seizures_start_time - 1)

		# read next line
		last_line = line
		line = summary_file.readline() 
		line_no += 1

	num_preictal_files = label_dict['Class'].count('Preictal')
	num_interictal_files = label_dict['Class'].count('Interictal')

	preictal_set = ['Test'] * (num_preictal_files//2) + ['Train'] * ((num_preictal_files//2) + (num_preictal_files%2))
	interictal_set = ['Test'] * (num_interictal_files//2) + ['Train'] * ((num_interictal_files//2) + (num_interictal_files%2))

	random.shuffle(preictal_set)
	random.shuffle(interictal_set)

	label_dict['Set'] = []

	for file_class in label_dict['Class'] :

		if file_class == 'Preictal' : label_dict['Set'].append(preictal_set.pop())

		elif file_class == 'Interictal' : label_dict['Set'].append(interictal_set.pop())

	# print(label_dict)

	temp_df = pd.DataFrame(label_dict)

	global df

	df = pd.concat([df, temp_df])

if __name__ == '__main__' :

	# Path to the EEG Data in edf format
	eeg_data_path = 'E:/Semester 2/IN 791/physionet.org/files/chbmit/1.0.0/'

	patient_ids = ['chb01', 'chb02', 'chb03']

	for patient_id in patient_ids :
		
		readSummaryFile(getSummaryFilePath(patient_id, eeg_data_path), patient_id)

	df.sort_values(by = ['Class', 'Case', 'Set'], ascending=[False, True, False], inplace=True)
	df.reset_index(inplace=True, drop=True)
	# print(df)
	df.to_excel('train_test_data.xlsx', index=False)
