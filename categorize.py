from dataset import EEG_Channels

columns = [
	'f_name',
	't_start',  # Global time in seconds
	't_end',    # Global time in seconds
	'num_seizures',
	't_seizure_start',	# Local file time in seconds
	't_seizure_end',	# Local file time in seconds
]

def getSeconds(time_str:str) -> int :
	'''Convert time in hh:mm:ss format to seconds'''

	hours, minutes, seconds = map(int, time_str.split(':'))

	return hours * 3600 + minutes * 60 + seconds

class FieldNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Field \"" + field_name + "\" not found in line \"" + line + "\".")

class ValueNotFoundError(Exception) :

	def __init__(self, field_name:str, line:str) -> None:
		
		super().__init__("Value for the field \"" + field_name + "\" not found in line \"" + line + "\".")

def readField(line:str, field_name:str) -> str :

	words = list(map(strip, line.split(':')))

	try					: index = words.index(field_name)
	except ValueError	: raise FieldNotFoundError(field_name, line)

	if index < len(words) - 1 :

		return words[index+1]
	
	else :

		raise ValueNotFoundError(field_name, line)

def readCheckChannels(file) :

	line = file.readline()

	try							: readField(line, "Channels in EDF Files")
	except ValueNotFoundError	: pass

	line = file.readline()	# This line would contain "*****************"
	line = file.readline()

	channel_no = 0

	master_channel_list = list(EEG_Channels).reverse()

	dummy_channels = []

	while channels :

		try :

			channel_no += 1
			channel_name = readField(line, "Channel %d".format(channel_no))

			if channel_name == '-' :
				
				dummy_channels.append(channel_no)
				continue

			if channel_name != master_channel_list.pop() :

				return False







def readCaseSummaryTxt(summary_file_path:str) -> dict :
    
	file_summary = dict()

	for field in columns :

		file_summary[field] = []

	

    pass
