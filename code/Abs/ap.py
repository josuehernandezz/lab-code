import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import helper as hp
import abs.utils as ut

sample = 'EB07'

# Absorbance file paths
abs_paths = '''
/Users/josuehernandez/Downloads/EB07_stockdil_70ul_3mlhex_Absorbance__0__19-05-07-073.txt
'''.split()

# Photoluminescence file paths
pl_paths = '''
/Users/josuehernandez/Downloads/EB07_PL_Subt2__0__12-44-29-036.txt
'''.split()

for i, path in enumerate(abs_paths):
    abs_path = hp.path2df(abs_paths[i])
    pl_path = hp.path2df(pl_paths[i])

    abs_wavelength = abs_path.column_1
    abs_intensity = abs_path.column_2
    abs_intensity_norm = hp.norm(abs_intensity, abs_wavelength, 300)

    pl_wavelength = pl_path.column_1
    pl_intensity = pl_path.column_2
    pl_intensity_norm = hp.norm(pl_intensity)

    # Calculate NC concentration
    absorbance = ut.get_absorbance(abs_wavelength, abs_intensity)
    print('Absorbance: ', absorbance)
    ut.calculate_concentration(absorbance, pl_intensity, pl_max_wavelength=511, dilution_factor=True, v_1=70, v_2=3070)

    if i == 0:
        i = ''
    plt.plot(abs_wavelength, abs_intensity_norm, label=f'Abs {i}')
    plt.plot(pl_wavelength, pl_intensity_norm, label=f'PL {i}')
    ut.fwhm(pl_wavelength, pl_intensity)
    ut.plotMaxPoint(pl_wavelength, pl_intensity_norm, 450, 550)

plt.xlim([300, 700])
plt.ylim([0, 1.02])
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.title(f'Absorbance and Photoluminescence of {sample}')
plt.legend()
plt.show()
