EEG_dataset_path = "D:\\Jagruti's Docs\\IN719\\CHB-MIT-EEG-Data"

save_path = "D:\\Jagruti's Docs\\IN719\\data"

preictal_period = 15 * 60 # seconds

window_len = 1000 # No of samples (time data points) input to ML model per channel

cases = [
    # "chb01",
	# "chb02",
	# "chb03",
	# "chb04",
	# "chb05",
    # "chb06",
	# "chb07",
	# "chb08",
	# "chb09",
	# "chb10",
    # "chb11",
	"chb12",
	# "chb13",
	# "chb14",
	# "chb15",
    # "chb16",
	# "chb17",
	# "chb18",
	# "chb19",
	# "chb20",
    # "chb21",
    # "chb22"
]

EEG_Channels = (
    'FP1-F7',
	'F7-T7',
	'T7-P7',
	'P7-O1',
	'FP1-F3',
	'F3-C3',
	'C3-P3',
	'P3-O1',
	'FZ-CZ',
	'CZ-PZ',
	'FP2-F4',
	'F4-C4',
	'C4-P4',
	'P4-O2',
	'FP2-F8',
	'F8-T8',
	'P8-O2',
	'P7-T7',
	'T7-FT9',
	'FT9-FT10',
	'FT10-T8'
)