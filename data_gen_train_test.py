import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import mne
import random
import string

root = 'E:/Semester 2/IN 791/physionet.org/files/chbmit/1.0.0' # pointer to where all data is stored
saveroot = 'data/' # pointer to where you wish to store train / test data
savefmt = '.npy' # save files in numpy's native format for arrays

print('Reading database:', root)
print('Saving core train/test data:', saveroot)

def get_cropped_data(filepath, start, end) -> np.ndarray:
    data = mne.io.read_raw_edf(input_fname=filepath, preload=False, verbose='Error') \
                 .crop(tmin=start, tmax=end) \
                 .get_data(picks='all', units='uV', return_times=False)
    return data

df = pd.read_excel('E:\\Semester 2\\IN 791\\physionet.org\\Codes\\train_test_data.xlsx')

# core data generation loop
with tqdm(total=len(df)) as pbar:
    identifier = ['A', 'B', 'C'] # generate filename for Train -> chb06 -> preictal
    counter = 0
    for index, row in df.iterrows():
        case = row['Case']
        filename = row['Filename']
        sset = row['Set']
        cclass = row['Class']
        crop_start = row['Crop Start']
        crop_end = row['Crop End']

        if sset == 'Train':
            if case == 'chb01':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
            if case == 'chb02':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + identifier[counter] + '_' + cclass.lower() + savefmt
                    counter += 1
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
            if case == 'chb03':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
        if sset == 'Test':
            if case == 'chb01':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
            if case == 'chb02':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
            if case == 'chb03':
                if cclass == 'Preictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
                if cclass == 'Interictal':
                    readpath = root + '/' + case + '/' + filename
                    data = get_cropped_data(readpath, int(crop_start), int(crop_end))
                    writedir = saveroot + '/' + sset + '/' + case + '/' + cclass
                    Path(writedir).mkdir(parents=True, exist_ok=True)
                    writepath = writedir + '/' + filename.split('.')[0] + '_' + cclass.lower() + savefmt
                    np.save(writepath, data)
        pbar.update(1)