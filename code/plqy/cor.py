# This python module is designed to take in a path to a file and return a text file that contains the 
# correction for an integrating sphere. 

import helper as h
from scipy.interpolate import pchip_interpolate
from matplotlib import pyplot as plt
import numpy as np

# Lamp spectral response
man_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/correction_files/manufacturer/Calibration_file_7003P2385_HL-3 plus-INT-CAL_int_20230727_VIS.txt'

# Raw calibration Data paths
sphere_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/IntegratingSphere/2024/7.24/7.15.24/calibration/calibration_1_0TO4A'
ocean_path = '/Volumes/JH-RESEARCH/Research/calibration/calibration1_Subt2__0__11-00-39-620.txt'
# pico_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/PicoQuant/2024/7.24/calibration_lamp/7.22.24_calibration_lamp/Plot.dat'

man_data = h.path2df(man_path)
sphere_data = h.path2df(sphere_path)
ocean_data = h.path2df(ocean_path)
# pico_data = h.path2df(pico_path)

man_x = man_data.iloc[:, 0]
man_y = man_data.iloc[:, 1]

sphere_x = sphere_data.iloc[:, 0]
sphere_y = sphere_data.iloc[:, 1]

ocean_x = ocean_data.iloc[:, 0]
ocean_y = ocean_data.iloc[:, 1]

# pico_x = pico_data.iloc[:, 0] / (10**-9)
# pico_y = pico_data.iloc[:, 3]

start = h.index(ocean_x, 350)
end = h.index(ocean_x, 700)
# i = h.index(pico_x, 700)

# Interpolates new data points in the data given by manufacturer so we can divide the raw data to manufacturer
man_y_interp = pchip_interpolate(man_x, man_y, sphere_x)
# pico_y_interp = pchip_interpolate(pico_x[:i], pico_y[:i], sphere_x)
ocean_y_interp = pchip_interpolate(ocean_x[start:end], ocean_y[start:end], sphere_x)

corrected_sphere = sphere_y / (man_y_interp * sphere_x)
corrected_sphere_ocean = sphere_y / (ocean_y_interp * sphere_x)

# calib_y_interp = pchip_interpolate(pico_x, pico_y, sphere_x)

####### Normalized

# plt.plot(man_x, (man_y / np.max(man_y)), label='Manufacturer')
# plt.plot(sphere_x, sphere_y / np.max(sphere_y), label='Sphere')
# plt.plot(ocean_x[start:end], ocean_y[start:end] / np.max(ocean_y[start:end]), label='Ocean Optics')
# plt.plot(pico_x[:i], pico_y[:i] / np.max(pico_y[:i]), label='Pico Quant')
# plt.plot(sphere_x, pico_y_interp / np.max(pico_y_interp), label='Pico Interp')
# plt.plot(sphere_x, corrected_sphere, label='Correction factor')

i = h.index(sphere_x, 356)

####### Raw
# plt.plot(sphere_x, man_y_interp, label='Manufacturer')
# plt.plot(sphere_x, sphere_y, label='Sphere')
y = sphere_y / man_y_interp
y = y[i:]
z = sphere_y / ocean_y_interp
z = z[i:]
sphere_x = sphere_x[i:]
sphere_y = sphere_y[i:]
corrected_sphere = corrected_sphere[i:]
man_y_interp_y = man_y_interp[i:]
man_y_interp_x = man_y_interp[i:] * sphere_x

# plt.plot(sphere_x, man_y_interp_y / np.max(man_y_interp_y), label='manufaturer')
# plt.plot(sphere_x, man_y_interp_x / np.max(man_y_interp_x), label='manufaturer * x')
# plt.plot(sphere_x, sphere_y / np.max(sphere_y), label='sphere')


# plt.plot(sphere_x, corrected_sphere / np.max(corrected_sphere), label='Correction * x')
# plt.plot(sphere_x, y / np.max(y), label='Correction')


plt.plot(sphere_x, corrected_sphere_ocean[i:] / np.max(corrected_sphere_ocean[i:]), label='Ocean Correction * x')
plt.plot(sphere_x, z / np.max(z), label='ocean correction')

plt.xlim([350, 700])
# plt.legend()
# plt.show()

######################## Text file Save ########################

data = np.column_stack((sphere_x, corrected_sphere_ocean[i:]))
save_txt_name = '7.22.24_ocean_correction_x.txt'
save_txt_path = '/Users/josuehernandez/Downloads/Correction/' + save_txt_name
np.savetxt(save_txt_path, data, delimiter=',') # Save text file
