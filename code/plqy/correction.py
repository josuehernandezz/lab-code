from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import pchip_interpolate

import helper as h
import temp_helper as th

# Lamp spectral response
# OLD
lamp_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/correction_files/manufacturer/Calibration_file_7003P2385_HL-3 plus-INT-CAL_int_20230727_VIS.txt'
# NEW
lamp_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/correction_files/manufacturer/8.13.24_ocean_insight_calibration/7003P2385_HL-3 plus-INT-CAL_int_20240813-153519_VIS.lmp'

# Raw calibration Data paths
calib_path = '/Users/josuehernandez/Downloads/DET100A2_calib_370_950_000.ssdat'
calib_path = '/Users/josuehernandez/Downloads/PDA100A2_70dB_calib_370_950_0TO2A'

lamp_data = h.path2df(lamp_path)
calib_data = h.path2df(calib_path)

lamp_x = lamp_data.iloc[:, 0]
lamp_y = lamp_data.iloc[:, 1]

calib_x = calib_data.iloc[:, 0]
calib_y = calib_data.iloc[:, 1]

# Interpolates new data points in between the original
lamp_y_interp = pchip_interpolate(lamp_x, lamp_y, calib_x)
calib_y_interp = pchip_interpolate(calib_x, calib_y, calib_x)

new_corr_y = calib_y_interp / lamp_y_interp

######################## Plots for Original Spectral Radiance ########################

# plt.plot(lamp_x,lamp_y, 'ro', label='Original')
# plt.plot(calib_x, lamp_y_interp, label='PCHIP')

# # Plot labels for Raw Spectral Radiance
# plt.xlim([350, 750])
# plt.title('Spectral Radiance of Deuterium and Tungsten Halogen Lamp')
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Radiance (µW/nm)')
# plt.legend()

######################## Plots for Raw Calibration spectra ########################

i = h.index(calib_x, 600)
# Choose an index slightly grater than zero due to abnormally high signal at 0
j = 0

# plt.plot(calib_x[j:], calib_y[j:], 'b', label='PDA100A2-10avg')

# plot below 600
# plt.plot(calib_x[j:i], calib_y[j:i]/np.max(calib_y[j:i]), 'b', label='PDA')
# plt.plot(calib_x[j:i], lamp_y_interp[j:i]/np.max(lamp_y_interp[j:i]), 'b', label='Manufacturer')
# plt.xlim([350, 600])

# plot above 600
# plt.plot(calib_x[i:], calib_y[i:], 'b', label='DET100A2')
# plt.plot(calib_x[i:], calib_y2[i:], 'r', label='PDA100A2')
# plt.xlim([600, 1000])

# Plot labels for Raw Calibration data files
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))  # Set y-axis to scientific notation
# plt.ticklabel_format(axis='x', style='plain')  # Leave x-axis unchanged
# plt.title('Raw Calibration')
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Intensity (V)')
# plt.legend()

######################## Plots for New Correction Factors ########################

plt.plot(calib_x[j:], h.norm(new_corr_y[j:]), 'r', label='New Correction')

# plt.plot(calib_x[j:], new_corr_y, 'r', label='New Correction')

# Plot labels for Raw Calibration data files
plt.xlim([350, 600])
plt.title('Correction Factor (a.u.)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (V)')
plt.legend()

######################## Text file Save ########################

data = np.column_stack((calib_x, new_corr_y))
save_txt_name = '9.11.24_PDA_correction.txt'
save_txt_path = '/Users/josuehernandez/Downloads/' + save_txt_name
np.savetxt(save_txt_path, data, delimiter=',') # Save text file

######################## Figure file Save ########################

# save_fig_name = '6.24.24-New-correction'
# save_fig_path = '/Users/josuehernandez/Downloads/' + save_fig_name
# plt.savefig(save_fig_path, dpi=1200) # Save Figure

plt.show()
