from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import pchip_interpolate

import helper as h
import temp_helper as th

# Lamp spectral response
manufacturer_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/correction_files/manufacturer/8.13.24_ocean_insight_calibration/7003P2385_HL-3 plus-INT-CAL_int_20240813-153519_VIS.lmp'

# Raw calibration Data paths
measurement_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/IntegratingSphere/2024/9.24/9.11.24/calibration/DET_370_950_redo_ensure_detector_on_001.ssdat'

# Extract data from files
manufacturer_data = h.path2df(manufacturer_path)
measurement_data = h.path2df(measurement_path)

# Get x and y columns and store them in their respective variables
manufacturer_x = manufacturer_data.iloc[:, 0]
manufacturer_y = manufacturer_data.iloc[:, 1]

# Get x and y columns and store them in their respective variables
measurement_x = measurement_data.iloc[:, 0]
measurement_y = measurement_data.iloc[:, 1]

# Interpolate new data points in between the original
manufacturer_y_interp = pchip_interpolate(manufacturer_x, manufacturer_y, measurement_x)

correction_y = measurement_y / manufacturer_y_interp

######################## Plots for New Correction Factors ########################

plt.plot(measurement_x, h.norm(correction_y), 'r', label='New Correction')

plt.xlim([350, 600])
plt.title('Correction Factor')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Correction Factor (r.u.)')
plt.legend()

######################## Text file Save ########################

file_name = '9.11.24_DET_latest_correction'
h.plot2txt(measurement_x, correction_y, file_name)

######################## Figure file Save ########################
fig_name = '9.11.24_correction_DET_Rerun'
# h.save_fig(fig_name)

plt.show()
