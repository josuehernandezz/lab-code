import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

abs_path = '/Users/josuehernandez/Downloads/MM01_40uL_2mL_Absorbance_Absorbance__0__16-29-15-304.txt'

abs_data = pd.read_csv(abs_path, delimiter='\t', names=('wavelength', 'intensity'), skiprows=14)

abs_wavelength = abs_data.wavelength
abs_intensity = abs_data.intensity
abs_intensity = abs_intensity / np.max(abs_intensity)


plt.plot(abs_wavelength, abs_intensity)
plt.title("MM01")
plt.ylabel("Intensity (a.u.)")
plt.xlabel("Wavelength (nm)")
# plt.xlim([300, 700])
plt.show()
