import numpy as np
from scipy.signal import welch
from scipy.integrate import simpson

import Parameters

bands = {
      'Delta'		: [0.1,	4.],
      'Theta'		: [4.,	8.],
      'Alpha'		: [8.,	12.],
      'Beta'		: [12.,	30.],
      'Low Gamma'	: [30.,	70.],
      'High Gamma'	: [70.,	127.],
}

sampling_freq = 256.
nperseg = min(Parameters.window_len, (2. / bands['Delta'][0]) * sampling_freq)

def compute_psd(signal_data:np.ndarray) -> np.ndarray :
    
	freqs, psd = welch(signal_data, sampling_freq, nperseg=nperseg, axis=1)
	freq_res = freqs[1] - freqs[0]

	bp = np.zeros((len(Parameters.EEG_Channels), len(bands.keys())))

	for i, band_name in enumerate(bands.keys()) :

		low, high = bands[band_name]

		bp[:, i] = simpson(psd[:, np.logical_and(freqs >= low, freqs <= high)], dx=freq_res, axis=1)

	bp = bp / bp.sum(axis=1, keepdims=True)

	return bp

	