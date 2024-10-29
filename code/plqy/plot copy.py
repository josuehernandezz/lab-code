import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid

import plqy_helper as hp

sample = 'Lead Oleate'
sample_Detail = sample
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
corr_path_conc = '/Users/josuehernandez/Downloads/lead_oleate_solid_test_save.csv'
############################## Importing ##############################
# # DELIMITER MAY BE DIFFERENT
# try:
#     cor_conc = pd.read_csv(corr_path_conc, delimiter=',', names=('wavelength', 'voltage'))
#     cor_dil = pd.read_csv(corr_path_dil, delimiter=',', names=('wavelength', 'voltage'))
#     try:
#         cor_conc = hp.path2df(corr_path_conc)
#         cor_dil = hp.path2df(corr_path_dil)
#     except Exception as e:
#         print(f"The following error occured:{e}")
# except Exception as e:
#     print(f"The following error occured:{e}")
#     print("Could not plot the given text files.")

cor_conc = hp.path2df(corr_path_conc)

# IF RAW INTEGRATING SPHERE DATA
cor_x1 = cor_conc.column_1
cor_y1 = cor_conc.column_2


# IF OTHER TEXT FILE SUCH AS UV-VIS
# cor_x1 = cor_conc.wavelength
# cor_y1 = cor_conc.voltage

# cor_x2 = cor_dil.wavelength
# cor_y2 = cor_dil.voltage

plt.plot(cor_x1, cor_y1, label='Blank')

plt.title('Lead Oleate IR Spectra')
plt.ylabel('% Transmittance')
plt.xlabel('Wavenumber (1/cm)')
plt.legend()

# save_fig_name = 'KL28SCN'
# save_fig_path = '/Users/josuehernandez/Downloads/' + save_fig_name
# plt.savefig(save_fig_path, dpi=1200) # Save Figure

plt.show()