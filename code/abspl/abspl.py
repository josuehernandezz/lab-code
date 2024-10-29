import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import helper as h


abs_path = '/Users/josuehernandez/Research/UV-Vis/JH01/Abs_JH01_50_8000_Absorbance__0__15-39-53-590.txt'
pl_path = '/Users/josuehernandez/Research/UV-Vis/JH01/PL_JH01_50_8000_white_Subt13__0__15-46-29-979.txt'

# Get the data from the file path and create two columns called wavelength and intensity
abs_data = pd.read_csv(abs_path, delimiter='\t', names=('wavelength', 'intensity'))
pl_data = pd.read_csv(pl_path, delimiter='\t', names=('wavelength', 'intensity'))

abs_wavelength = abs_data.wavelength
abs_intensity = abs_data.intensity

pl_wavelength = pl_data.wavelength
pl_intensity = pl_data.intensity

abs_intensity_norm = (abs_intensity / (np.max(abs_intensity)))
pl_intensity_norm = (pl_intensity / np.max(pl_intensity))

# Calculates the Perovskite NC concentration
absorbance = h.calculate_absorbance(abs_wavelength, abs_intensity)
nc_conc = h.calculate_concentration(absorbance, pl_intensity, 8.2)

v_1 = 50 # uL
m_2 = nc_conc # concentration of the diluted NCs
v_2 = 8050 # total volume of hexane added in uL + 50uL of NC initially
m_1 = (m_2 * v_2) / v_1

plt.plot(abs_wavelength, abs_intensity_norm, label='Abs')
plt.plot(pl_wavelength, pl_intensity_norm, label='PL')
plt.title('UV-Vis JH01')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.xlim([300, 700])
plt.ylim([0, 1])
plt.legend()
plt.show()
