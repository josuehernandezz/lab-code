import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid

from . import plqy_helper as hp


sample = 'KL28SCN'
sample_Detail = sample + ' Film'
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
plot_1 = '/Users/josuehernandez/Downloads/Data 2/blank_hexane_000.ssdat'
plot_2 = '/Users/josuehernandez/Downloads/Data 2/dilute_1_stock_000.ssdat'
plot_3 = '/Users/josuehernandez/Downloads/Data 2/dilute_4_250uL_2mL_000.ssdat'

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

plot_1 = hp.path2df(plot_1)
plot_2 = hp.path2df(plot_2)
plot_3 = hp.path2df(plot_3)

# IF RAW INTEGRATING SPHERE DATA
plot_1_x = plot_1.column_1
plot_1_y = plot_1.column_2

plot_2_x = plot_2.column_1
plot_2_y = plot_2.column_2

plot_3_x = plot_3.column_1
plot_3_y = plot_3.column_2

# IF OTHER TEXT FILE SUCH AS UV-VIS
# cor_x1 = cor_conc.wavelength
# cor_y1 = cor_conc.voltage

# cor_x2 = cor_dil.wavelength
# cor_y2 = cor_dil.voltage

plt.plot(plot_1_x, plot_1_y, label='Blank')
plt.plot(plot_3_x, plot_3_y, label='Concentrated')
plt.plot(plot_2_x, plot_2_y, label='Dilute')

# plt.title('KL28SCN Film')
plt.ylabel('Intensity (V)')
plt.xlabel('Wavelength (nm)')
plt.legend()

# save_fig_name = 'KL28SCN_film_spectra'
# save_fig_path = '/Users/josuehernandez/Downloads/' + save_fig_name
# plt.savefig(save_fig_path, dpi=1200) # Save Figure

plt.show()
