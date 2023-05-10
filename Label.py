import os
import pandas as pd

import Parameters
from modules.Read_CHB_Summary_TXT import readCaseSummaryTxt

df = pd.DataFrame()

for case_id in Parameters.cases :
    
	summary_file_path = os.path.join(Parameters.EEG_dataset_path, case_id, case_id + '-summary.txt')

	try :

		summary_dict = readCaseSummaryTxt(summary_file_path)

		summary_dict['case'] = [case_id] * len(summary_dict['f_name'])

		temp_df = pd.DataFrame(summary_dict)
		df = pd.concat([df, temp_df])

	except EOFError :

		print('Case \"' + case_id + '\" does not contain channels according to the channel list in Parameters.py')
		
# print(df)

save_file_path = os.path.join(Parameters.save_path, "signal-labels.csv")
df.to_csv(save_file_path, ',', index=False)