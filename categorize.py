import dataset

columns = [
	'f_name',
	't_start',  # Global time in seconds
	't_end',    # Global time in seconds
	'class',	# Ictal, Preictal, Interictal
]

def getSeconds(time_str:str, days:int=0) -> int :
	'''Convert time in hh:mm:ss format to seconds'''

	hours, minutes, seconds = map(int, time_str.split(':'))

	ret_days = days
	if hours > 23 : ret_days += 1

	return hours * 3600 + minutes * 60 + seconds + 24 * 3600 * days, ret_days

class FieldNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Field \"" + field_name + "\" not found in line \"" + line + "\".")

class ValueNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Value for the field \"" + field_name + "\" not found in line \"" + line + "\".")

def readField(line:str, field_name:str) -> str :

	words = list(map(str.strip, line.split(': ')))

	try					: index = words.index(field_name)
	except ValueError	: raise FieldNotFoundError(field_name, line)

	if index < len(words) - 1 :	return words[index+1]
	else :	raise ValueNotFoundError(field_name, line)

def readChannels(file) -> list :

	indices_list = []

	channel_no = 0
	reqd_channel_list = list(dataset.EEG_Channels)
	reqd_channel = reqd_channel_list.pop(0)

	while True :
	
		try :
			
			line = file.readline()
			if not line : raise EOFError("Reached end of file during channel read.")

			channel_no += 1
			channel_name = readField(line, 'Channel ' + str(channel_no))
			
			if channel_name == reqd_channel :
			
				indices_list.append(channel_no-1)
				reqd_channel = reqd_channel_list.pop(0)
		
		except (FieldNotFoundError, IndexError) :

			break

	return indices_list

def appendChannels(file_summary_dict:dict, reqd_channels_indices:list) :

	for EEG_channel_no, channel_number in zip(range(len(dataset.EEG_Channels)), reqd_channels_indices) :

			file_summary_dict[EEG_channel_no].append(channel_number)

	pass

def readCaseSummaryTxt(file_path:str) -> dict :
    
	file = open(file_path)

	file_summary = dict()
	for field in columns : file_summary[field] = []
	for field in range(len(dataset.EEG_Channels)) : file_summary[field] = []
	
	reqd_channels_indices = readChannels(file)
	
	while len(reqd_channels_indices) != 23 :
	
		reqd_channels_indices = readChannels(file)

	days = 0

	# Read first line
	line = file.readline()
	
	while line :

		try :

			readField(line, 'Channels changed')

		except ValueNotFoundError :

			reqd_channels_indices = readChannels(file)
	
			while len(reqd_channels_indices) != 23 :
			
				reqd_channels_indices = readChannels(file)

		except FieldNotFoundError :

			pass

		try :

			edf_file_name = readField(line, 'File Name')

		except FieldNotFoundError :
			
			line = file.readline()
			continue

		# read next line
		line = file.readline() 
		start_time, days = getSeconds(readField(line, 'File Start Time'), days)

		# read next line
		line = file.readline()
		end_time, days = getSeconds(readField(line, 'File End Time'), days)

		# read next line
		line = file.readline()
		num_seizures = int(readField(line, 'Number of Seizures in File'))

		if num_seizures == 0 :

			# Fill data into dictionary
			file_summary['f_name'].append(edf_file_name)
			file_summary['class'].append('Interictal')
			file_summary['t_start'].append(start_time)
			file_summary['t_end'].append(end_time)

			appendChannels(file_summary, reqd_channels_indices)

		elif num_seizures == 1 :

			# read next line
			line = file.readline() 

			try :						seizures_start_time = int(readField(line, 'Seizure Start Time').split()[0])
			except FieldNotFoundError :	seizures_start_time = int(readField(line, 'Seizure 1 Start Time').split()[0])
			
			# read next line
			line = file.readline() 

			try :						seizures_end_time = int(readField(line, 'Seizure End Time').split()[0])
			except FieldNotFoundError :	seizures_end_time = int(readField(line, 'Seizure 1 End Time').split()[0])

			# Fill Preictal data into dictionary
			preictal_start_time = start_time + seizures_start_time - dataset.preictal_period
			preictal_end_time = start_time + seizures_start_time

			if preictal_start_time > start_time :
				
				file_summary['f_name'].append(edf_file_name)
				file_summary['class'].append('Preictal')
				file_summary['t_start'].append(preictal_start_time)
				file_summary['t_end'].append(preictal_end_time)

				appendChannels(file_summary, reqd_channels_indices)

			else : # Preictal period starts from the beginning of the file

				try :
				
					if preictal_start_time < file_summary['t_end'][-1] : # The last file contains a segment of preictal period

						prev_file_end_time = file_summary['t_end'][-1]
						file_summary['t_end'][-1] = preictal_start_time

						file_summary['f_name'].append(file_summary['f_name'][-1])
						file_summary['class'].append('Preictal')
						file_summary['t_start'].append(preictal_start_time)
						file_summary['t_end'].append(prev_file_end_time)

						for field in range(len(dataset.EEG_Channels)) : file_summary[field].append(file_summary[field][-1])

				except IndexError : pass

				file_summary['f_name'].append(edf_file_name)
				file_summary['class'].append('Preictal')
				file_summary['t_start'].append(start_time)
				file_summary['t_end'].append(preictal_end_time)

				appendChannels(file_summary, reqd_channels_indices)

			# Fill Ictal data into dictionary
			file_summary['f_name'].append(edf_file_name)
			file_summary['class'].append('Ictal')
			file_summary['t_start'].append(start_time + seizures_start_time)
			file_summary['t_end'].append(start_time + seizures_end_time)

			appendChannels(file_summary, reqd_channels_indices)

		# read next line
		line = file.readline() 

	file.close()
	
	return file_summary

if __name__ == '__main__' :

	import os, pandas

	my_dict = readCaseSummaryTxt(os.path.join(dataset.path, dataset.cases[0], dataset.cases[0] + '-summary.txt'))

	print(pandas.DataFrame(my_dict))
