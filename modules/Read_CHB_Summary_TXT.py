import modules.Seizure_Period as Seizure_Period

from Parameters import preictal_period

columns = set([
	'File Name',
	'Period Label',
	'Period Start Time',	# Local time in seconds
	'Period End Time',		# Local time in seconds
	'File Start Time'		# Global time in seconds
])

def getSeconds(time_str:str, days:int=0) -> float :
	'''Convert time in hh:mm:ss format to seconds'''

	hours, minutes, seconds = map(int, time_str.split(':'))

	ret_days = days
	if hours > 23 : ret_days += 1

	return hours * 3600 + minutes * 60 + seconds + 24 * 3600 * days, ret_days

class FieldNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Field \"" + field_name + "\" not found in line \"" + line.strip() + "\".")

class ValueNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Value for the field \"" + field_name + "\" not found in line \"" + line.strip() + "\".")

def readField(line:str, field_name:str) -> str :

	words = list(map(str.strip, line.split(': ')))

	try					: index = words.index(field_name)
	except ValueError	: raise FieldNotFoundError(field_name, line)

	if index < len(words) - 1 :	return words[index+1]
	else :	raise ValueNotFoundError(field_name, line)

def addToFileDictionary(dictionary:dict, f_name:str, p_start:float, p_end:float, p_label:Seizure_Period.label, f_start:float) :

	dictionary['File Name'].append(f_name)
	dictionary['Period Label'].append(p_label.value)
	dictionary['Period Start Time'].append(p_start)
	dictionary['Period End Time'].append(p_end)
	dictionary['File Start Time'].append(f_start)

	pass

def readCaseSummaryTxt(file_path:str) -> dict :
    
	file = open(file_path)

	periods = dict()
	for field in columns : periods[field] = []

	days = 0
	last_read_time = -1

	# Read first line
	line = file.readline()

	while line :

		try :

			edf_file_name = readField(line, 'File Name')

		except FieldNotFoundError :
			
			line = file.readline()
			continue

		# read next line
		line = file.readline() 
		start_time, days = getSeconds(readField(line, 'File Start Time'), days)
		if last_read_time > start_time :
			days += 1
			start_time += 3600 * 24
		last_read_time = start_time

		# read next line
		line = file.readline()
		end_time, days = getSeconds(readField(line, 'File End Time'), days)
		if last_read_time > end_time :
			days += 1
			end_time += 3600 * 24
		last_read_time = end_time

		# read next line
		line = file.readline()
		num_seizures = int(readField(line, 'Number of Seizures in File'))

		if num_seizures == 0 :

			# Fill data into dictionary
			addToFileDictionary(periods, edf_file_name, 0, end_time - start_time, Seizure_Period.label.Interictal, start_time)
			
		else :

			for seizure_no in range(1, num_seizures+1) :

				# read next line
				line = file.readline() 

				try :						seizures_start_time = int(readField(line, 'Seizure Start Time').split()[0])
				except FieldNotFoundError :	seizures_start_time = int(readField(line, 'Seizure ' + str(seizure_no) + ' Start Time').split()[0])
				
				# read next line
				line = file.readline() 

				try :						seizures_end_time = int(readField(line, 'Seizure End Time').split()[0])
				except FieldNotFoundError :	seizures_end_time = int(readField(line, 'Seizure ' + str(seizure_no) + ' End Time').split()[0])

				# Find preictal start and end times
				preictal_start_time = seizures_start_time - preictal_period
				preictal_end_time = seizures_start_time

				if seizure_no == 1 :
						
					if preictal_start_time > 0 :

						addToFileDictionary(periods, edf_file_name, 0, preictal_start_time, Seizure_Period.label.Interictal, start_time)

					elif preictal_start_time < 0 :

						last_period_global_stop_time = periods['Period End Time'][-1] + periods['File Start Time'][-1]
						preictal_global_start_time = preictal_start_time + start_time

						if preictal_global_start_time < last_period_global_stop_time :

							last_period_local_stop_time = preictal_global_start_time - periods['File Start Time'][-1]

							periods['Period End Time'][-1] = last_period_local_stop_time
							
							addToFileDictionary(
								periods,
								periods['File Name'][-1],
								last_period_local_stop_time,
								last_period_global_stop_time - periods['File Start Time'][-1],
								Seizure_Period.label.Preictal,
								periods['File Start Time'][-1]
							)

						preictal_start_time = 0

					addToFileDictionary(periods, edf_file_name, preictal_start_time, preictal_end_time, Seizure_Period.label.Preictal, start_time)

				else :

						if seizures_start_time < periods['Period Start Time'][-1] > preictal_period :
						
							periods['Period End Time'][-1] = preictal_start_time
							addToFileDictionary(periods, edf_file_name, preictal_start_time, preictal_end_time, Seizure_Period.label.Preictal, start_time)

						else :

							periods['Period Label'][-1] = Seizure_Period.label.Preictal.value
							periods['Period End Time'][-1] = preictal_end_time

				addToFileDictionary(periods, edf_file_name, seizures_start_time, seizures_end_time, Seizure_Period.label.Ictal, start_time)
				addToFileDictionary(periods, edf_file_name, seizures_end_time, end_time - start_time, Seizure_Period.label.Interictal, start_time)

		# read next line
		line = file.readline() 

	file.close()
	
	return periods