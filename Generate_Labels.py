import os
import pandas as pd

import Parameters
from modules.Read_CHB_Summary_TXT import readCaseSummaryTxt, FieldNotFoundError, ValueNotFoundError

df = pd.DataFrame()

for case_id in Parameters.cases :

	summary_file_path = os.path.join(Parameters.EEG_dataset_path, case_id, case_id + '-summary.txt')

	try :

		summary_dict = readCaseSummaryTxt(summary_file_path)

		summary_dict['Case'] = [case_id] * len(summary_dict['File Name'])

		summary_dict['Period Label'] = list(map(lambda x : x.name, summary_dict['Period Label']))

		temp_df = pd.DataFrame(summary_dict)
		df = pd.concat([df, temp_df])

	except (FieldNotFoundError, ValueNotFoundError) as e:

		print('Bad file read at \"' + summary_file_path + '\"')
		print(e)
		
# print(df)

save_file_path = os.path.join(Parameters.save_path, 'edf-file-period-labels.csv')
df.to_csv(save_file_path, ',', index=False)