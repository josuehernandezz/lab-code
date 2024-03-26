from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import pchip_interpolate

import helper as h
import temp_helper as th

# Lamp spectral response
lamp_path = '/Users/josuehernandez/Downloads/Calibration_file_7003P2385_HL-3 plus-INT-CAL_int_20230727_VIS.txt'

# Raw calibration Data paths
calib_path = '/Users/josuehernandez/Downloads/plqy_data/9th_calibration_000.ssdat'

# Old/Previous Correction Data
old_correction = '/Users/josuehernandez/Downloads/Correction.txt'

lamp_data = h.path2df(lamp_path)
calib_data = h.path2df(calib_path)
old_corr_data = h.path2df(old_correction)

lamp_x = lamp_data.iloc[:, 0]
lamp_y = lamp_data.iloc[:, 1]

calib_x = calib_data.iloc[:, 0]
calib_y = calib_data.iloc[:, 1]

old_corr_x = old_corr_data.iloc[:, 0]
old_corr_y = old_corr_data.iloc[:, 1]

# Interpolates new data points in between the original
lamp_y_interp = pchip_interpolate(lamp_x, lamp_y, old_corr_x)
calib_y_interp = pchip_interpolate(calib_x, calib_y, old_corr_x)

new_corr_y = calib_y_interp / lamp_y_interp

# plt.plot(lamp_x,lamp_y, 'ro', label='Lamp Spectral Response OG')
# plt.plot(calib_x, lamp_y_interp, label='Lamp Spectral Response PCHIP')

# plt.plot(calib_x, calib_y, 'b', label='Raw Calibration')

plt.plot(old_corr_x, h.norm(new_corr_y), 'r', label='New Correction')
plt.plot(old_corr_x, h.norm(old_corr_y), 'y', label='Old Correction')

# plt.plot(calib_x, new_corr_y, 'r', label='New Correction')
# plt.plot(old_corr_x, old_corr_y, 'y', label='Old Correction')

plt.xlim([350, 750])
plt.title('Correction Factor')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Correction Factor (a.u.)')
plt.legend()

# Text file Save
data = np.column_stack((old_corr_x, new_corr_y))
save_txt_name = '3.25.24_new_correction.txt'
save_txt_path = '/Users/josuehernandez/Downloads/' + save_txt_name
np.savetxt(save_txt_path, data, delimiter=',') # Save text file

# Figure file Save
save_fig_name = 'Correction_figs'
save_fig_path = '/Users/josuehernandez/Downloads/' + save_fig_name
plt.savefig(save_fig_path, dpi=1200) # Save Figure

plt.show()
