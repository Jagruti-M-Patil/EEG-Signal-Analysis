import numpy as np
# from scipy.linalg import toeplitz, lstsq
# from scipy.signal import correlate

import Parameters

order = 2

# Copied from samisnotinsane/chbmit-seizure-detection
def estimateARCoefficients(input_signal):

	ymat	= np.zeros((Parameters.window_len - order, order))	# (window_len - order) x order

	for _c in range(order, 0, -1) :

		ymat[ : , order - _c] = input_signal[order - _c : -_c]

	yb = input_signal[order:]	# (window_len - order) x 1

	#   ((order x order) . (order x (window_len - order))) . ((window_len - order) x 1)
	# = (order x (window_len - order)) . ((window_len - order) x 1)
	# = (order x 1)
	
	return np.linalg.pinv(ymat) @ yb
