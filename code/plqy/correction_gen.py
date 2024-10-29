# This python module is designed to take in a path to a file and return a text file that contains the 
# correction for an integrating sphere. 

import helper as h
from scipy.interpolate import pchip_interpolate
from matplotlib import pyplot as plt
import numpy as np

# Lamp spectral response
lamp_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/correction_files/manufacturer/Calibration_file_7003P2385_HL-3 plus-INT-CAL_int_20230727_VIS.txt'

lamp_path = '/Users/josuehernandez/jh_sheldon_group/data/IntegratingSphere/Calibration_file_7003P2385_HL-3 plus-INT-CAL_int_20230727_VIS.txt'
# lamp_path = '/Volumes/JH-RESEARCH/Research/calibration/calibration1_Subt2__0__11-00-39-620.txt'
# lamp_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/PicoQuant/2024/7.24/calibration_lamp/7.22.24_calibration_lamp/Plot.dat'

# Raw calibration Data paths
calib_path_sphere = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/IntegratingSphere/2024/7.24/7.15.24/calibration/calibration_1_0TO4A'
calib_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/PicoQuant/2024/7.24/calibration_lamp/7.22.24_calibration_lamp/Plot.dat'

calib_path_sphere = '/Users/josuehernandez/jh_sheldon_group/data/IntegratingSphere/2024/6.24/6.13.24/calibration/Calibration-1_000.ssdat'

lamp_data = h.path2df(lamp_path)
clib_data_sphere = h.path2df(calib_path_sphere)
calib_data = h.path2df(calib_path)

lamp_x = lamp_data.iloc[:, 0]
lamp_y = lamp_data.iloc[:, 1]

sphere_x = clib_data_sphere.iloc[:, 0]
sphere_y = clib_data_sphere.iloc[:, 1]

# plt.plot(lamp_x, lamp_data.iloc[:, 1], label='Col 1')
# plt.plot(lamp_x, lamp_data.iloc[:, 2], label='Col 2')
# plt.plot(lamp_x, lamp_data.iloc[:, 3], label='Col 3')

calib_x = calib_data.iloc[:, 0]
calib_y = calib_data.iloc[:, 3]

# Interpolates new data points in the data given by manufacturer so we can divide the raw data to manufacturer
lamp_y_interp = pchip_interpolate(lamp_x, lamp_y, sphere_x)
calib_y_interp = pchip_interpolate(calib_x, calib_y, sphere_x)

# Calculating the correction factor
new_corr_y = sphere_y / lamp_y_interp


# x2 = np.arange(380, 700, 1)
# calib_y_interp_2 = pchip_interpolate(calib_x, calib_y, x2)
# lamp_y_interp_2 = pchip_interpolate(lamp_x, lamp_y, x2)

######################## Text file Save ########################

# data = np.column_stack((calib_x, new_corr_y))
# save_txt_name = '7.17.24_new_correction.txt'
# save_txt_path = '/Users/josuehernandez/Downloads/Correction/' + save_txt_name
# np.savetxt(save_txt_path, data, delimiter=',') # Save text file

# plt.plot(sphere_x, lamp_y_interp / np.max(lamp_y_interp), label='manufaturer')
# plt.plot(sphere_x, sphere_y / np.max(sphere_y), label='sphere')
# plt.plot(calib_x, calib_y, label='Pico Quant')

# plt.plot(sphere_x, calib_y_interp, label='Interpolated')

# plt.plot(x2, lamp_y_interp_2 / np.max(lamp_y_interp_2), label='manufaturer')
# plt.plot(x2, calib_y_interp_2/np.max(calib_y_interp_2), label='sphere')
# plt.plot(x2, (calib_y_interp_2/np.max(calib_y_interp_2)) / (lamp_y_interp_2 / np.max(lamp_y_interp_2)), label='correction')

# plt.plot(calib_x, calib_y/np.max(calib_y), label='UV-VIS')
# plt.plot(calib_x, lamp_y_interp/np.max(lamp_y_interp), label='manufacturer')


new_corr_y = new_corr_y / np.min(new_corr_y)

plt.plot(sphere_x, new_corr_y)
plt.xlim([350, 600])
plt.legend()
plt.show()
