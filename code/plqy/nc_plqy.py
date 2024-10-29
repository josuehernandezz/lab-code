import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid

import plqy_helper as hp

sample = 'Coumarin 6'
sample_Detail = sample + ' in Ethanol'
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
corr_path = '/Users/josuehernandez/Downloads/9.11.24_DET_correction.txt'
# corr_path = '/Users/josuehernandez/Downloads/9.11.24_PDA_correction.txt'

blk_path = '/Volumes/JH-RESEARCH/Research/IntegratingSphere/2024/9.24/9.10.24/measurement/blank_hexane_440_590_000.ssdat'
dil_path = '/Volumes/JH-RESEARCH/Research/IntegratingSphere/2024/9.24/9.10.24/measurement/EB06_440_590_000.ssdat'

############################## Importing ##############################
# DELIMITER MAY BE DIFFERENT
cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))
blk= hp.path2df(blk_path) # Blank
dil = hp.path2df(dil_path) # True (Diluted)

################### Column Selection

cor_x = cor.wavelength
cor_y = cor.voltage

# interpolates the correction data to have as many data points as the raw data (# of x data points in the blank)
cor_interpolation = pchip_interpolate(cor_x, cor_y, blk.column_1)

blk_x = blk.column_1
blk_y = blk.column_2
# Apply correction factor to blank, and convert to photon counts
blk_y = blk_y * cor_interpolation * (blk_x * 10 ** -9)

dil_x = dil.column_1
dil_y = dil.column_2
dil_y_norm_1 = dil_y / np.max(dil_y)
dil_y_un_cor = dil_y
dil_y_un_cor_norm = dil_y_un_cor / np.max(dil_y_un_cor)
# Apply correction factor to dilute sample, and convert to photon counts
dil_y = dil_y * cor_interpolation * (dil_x * 10 ** -9)

####### Define Excitation integration region
ex_s = 440
ex_e = 480

####### Blank Excitation Integral
blk_exc_int = hp.integrate(blk_x, blk_y, ex_s, ex_e)

####### Dilute Excitation Integral
dil_exc_int = hp.integrate(dil_x, dil_y, ex_s, ex_e)

####### Conc Excitation Integral
# conc_exc_int = hp.integrate(conc_x, conc_y, ex_s, ex_e)

####### Define Emission integration region
emi_s = 480
emi_e = 589

####### Blank Emission Integral
blk_emi_int = hp.integrate(blk_x, blk_y, emi_s, emi_e)

####### Dilute Emission Integral
scale_factor = 1.1
dil_y_norm = (dil_y[emi_s:emi_e] / np.max(dil_y[emi_s:emi_e]))
dil_y_scaled = dil_y_norm * scale_factor

dil_emi_int = hp.integrate(dil_x, dil_y, emi_s, emi_e)

####### Concentrated Emission Integral
# conc_emi_int = hp.integrate(conc_x, conc_y, emi_s, emi_e)
# conc_norm_emi_int = hp.integrate(conc_x, conc_y_norm, emi_s, emi_e)

# Normalized emission of Concentrated sample, divided by the diluted scaled emission such that the red tails touch.
# a = 1 - (conc_norm_emi_int / dil_scaled_emi_int)

# plqy_observed = conc_emi_int / (blk_exc_int - conc_exc_int)
# plqy = (dil_emi_int - blk_emi_int) / (blk_exc_int - dil_exc_int)
# print(plqy)

plqy = (dil_emi_int) / (blk_exc_int - dil_exc_int)
print(plqy * 100)
# print(dil_emi_int)

# plqy = (plqy_observed / ((1 - a) + (a * plqy_observed))) * 100
# print('plqy', plqy)

# Plot the normal files

plt.plot(blk_x, blk_y, label='blank')
plt.plot(dil_x, dil_y, label='dilute')
# plt.plot(dil_x, dil_y_un_cor, label='uncorrected.')
# plt.plot(conc_x, conc_y, label='concentrated')

# plt.plot(dil_x[emi_s:emi_e], dil_y_norm, label='Dilute Normalized')
# plt.plot(conc_x[emi_s:emi_e], conc_y_norm[emi_s:emi_e], label='Concentrated Emission')
# plt.plot(dil_x[emi_s:emi_e], dil_y_scaled, label='Dilute Emission Scaled')

plt.title('Raw Lamp Spectrum')
plt.ylabel('Intensity a.u.')
plt.xlabel('Wavelength (nm)')
plt.legend()
plt.show()
