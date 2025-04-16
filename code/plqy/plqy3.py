import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid
from matplotlib.ticker import FormatStrFormatter

# import plqy_helper as hp
from . import plqy_helper as hp
import helper as h

sample = 'JH03_12.10.24'
sample_detail = sample + ' Colloid'
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
# corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/Calibration Lamp/correction_files/old_correction_data/Correction.txt'
corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_i.txt'

blk_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/IntegratingSphere/2025/1.25/1.20.25/coumarin6/blank_ethanol_000.ssdat'
dil_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/IntegratingSphere/2025/1.25/1.20.25/coumarin6/coumarin_6_000.ssdat'
# blk_path = '/Users/josuehernandez/Downloads/1.23.25 - calib - coumarin6/coumarin6/blank_ethanol_000.ssdat'
# dil_path = '/Users/josuehernandez/Downloads/1.23.25 - calib - coumarin6/coumarin6/coumarin_6_000.ssdat'

############################## Importing ##############################
# DELIMITER MAY BE DIFFERENT
cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))
# cor = pd.read_csv(corr_path, delimiter='\t', names=('wavelength', 'voltage'))
blk= hp.path2df(blk_path) # Blank
dil = hp.path2df(dil_path) # True (Diluted)

################### Column Selection
cor_x = cor.wavelength
cor_y = cor.voltage

# interpolates the correction data to have as many data points as the raw data (# of x data points in the blank)
cor_interpolation = pchip_interpolate(cor_x, cor_y, blk.column_1)[:-5]
# cor_interpolation = pchip_interpolate(cor_x, cor_y, blk.column_1)
cor_interpolation = cor_interpolation

# blk_x = blk.column_1
# blk_y = blk.column_2
blk_x = blk.column_1[:-5]
blk_y = blk.column_2[:-5]
# Apply correction factor to blank, and convert to photon counts
blk_y = blk_y * cor_interpolation * (blk_x * 10 ** -9)

dil_x = dil.column_1
dil_y = dil.column_2
# Apply correction factor to dilute sample, and convert to photon counts
dil_y = dil_y * cor_interpolation * (dil_x * 10 ** -9)

####### Define Excitation integration region
# # FOR COUMARIN 6 390 - 420
# ex_s = 390
# ex_e = 420
ex_s = 390
ex_e = 415

# FOR PNCs 440 - 460
# ex_s = 440
# ex_e = 460

####### Blank Excitation Integral
blk_exc_int = hp.integrate(blk_x, blk_y, ex_s, ex_e)

####### Dilute Excitation Integral
dil_exc_int = hp.integrate(dil_x, dil_y, ex_s, ex_e)

####### Define Emission integration region
# # FOR COUMARIN 6 460 - 680
emi_s = 460
emi_e = 625

# FOR PNCs 470 - 550
# emi_s = 470
# emi_e = 570

####### Blank Emission Integral
blk_emi_int = hp.integrate(blk_x, blk_y, emi_s, emi_e)

####### Dilute Emission Integral
dil_emi_int = hp.integrate(dil_x, dil_y, emi_s, emi_e)

####### Calculate dilute emission integral
dilute_plqy = (dil_emi_int) / (blk_exc_int - dil_exc_int)
print('Dilute plqy, not subtracting blank', dilute_plqy * 100)

dilute_plqy = (dil_emi_int - blk_emi_int) / (blk_exc_int - dil_exc_int)
print('Dilute plqy, minus blank', dilute_plqy * 100)

plt.plot(blk_x, blk_y, label='Blank')
plt.plot(dil_x, dil_y, label='Coumarin 6')
plt.legend()
plt.title('Coumarin 6')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (V)')
plt.plot()
# h.save_fig('Coumarin_6_conc')
plt.show()
