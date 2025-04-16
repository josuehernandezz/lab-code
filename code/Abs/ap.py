import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import helper as hp
import abs.utils as ut

sample = 'MM04'

# Absorbance file paths
abs_paths = '''
/Volumes/Data-1/Mara/MM04/04.10.25/MM04_abs_250uL_2mL_hex_fuchsia_10_Absorbance__0__13-17-06-892.txt
'''.split()

# Photoluminescence file paths
pl_paths = '''
/Volumes/Data-1/Mara/MM04/04.10.25/MM04_pl_250_uL_2_mL_white_25_Subt13__0__13-23-23-890.txt
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
    print('Absorbance @335: ', absorbance)
    ut.calculate_concentration(absorbance, pl_intensity, pl_max_wavelength=506, dilution_factor=False, v_1=200, v_2=2200)

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

# Uncomment to save figure with the specified file name in the downloads folder
hp.save_fig(f"{sample}_AbsPL")

plt.show()
