import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid
from matplotlib.ticker import FormatStrFormatter

# import plqy_helper as hp
from . import plqy_helper as hp
import helper

sample = 'EB07'
sample_detail = sample + ' in hexane'
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
# corr_path = '/Users/josuehernandez/Downloads/correction_factor.txt'
# corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_i.txt'
corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_inverted.txt'

# blk_path = '/Users/josuehernandez/Downloads/Data 2/blank_hexane_000.ssdat'
blk_path = '/Volumes/Data-1/josue/IntegratingSphere/MM/MM03/Hexane/blank_hexane_000.ssdat'
# dil_path = '/Users/josuehernandez/Downloads/Data 2/dilute_4_250uL_2mL_000.ssdat'
dil_path = '/Volumes/Data-1/josue/IntegratingSphere/MM/MM03/Hexane/dilute_MM03_hex_000.ssdat'
# conc_path = '/Users/josuehernandez/Downloads/Data 2/dilute_1_stock_000.ssdat'
conc_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/Measurements/PLQY/EB Samples/EB07/dilute_1_stock_000.ssdat'
conc_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/Measurements/PLQY/EB Samples/EB07/dilute_2_1mLstock_1mLHex_000.ssdat'
conc_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/Data/Measurements/PLQY/EB Samples/EB07/dilute_3_250uL_2mL_000.ssdat'

############################## Importing ##############################
# DELIMITER MAY BE DIFFERENT
cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))
blk= hp.path2df(blk_path) # Blank
dil = hp.path2df(dil_path) # True (Diluted)
conc = hp.path2df(conc_path) # True (Conc)

################### Column Selection
cor_x = cor.wavelength
cor_y = cor.voltage

# interpolates the correction data to have as many data points as the raw data (# of x data points in the blank)
cor_interpolation = pchip_interpolate(cor_x, cor_y, blk.column_1)
cor_interpolation = cor_interpolation

blk_x = blk.column_1
blk_y = blk.column_2
# Apply correction factor to blank, and convert to photon counts
blk_y = blk_y * cor_interpolation * (blk_x * 10 ** -9)

dil_x = dil.column_1
dil_y = dil.column_2
# Apply correction factor to dilute sample, and convert to photon counts
dil_y = dil_y * cor_interpolation * (dil_x * 10 ** -9)

conc_x = conc.column_1
conc_y = conc.column_2
conc_y = conc_y * cor_interpolation * (conc_x * 10 ** -9)

####### Define Excitation integration region
# # FOR COUMARIN 6
# ex_s = 390
# ex_e = 420

# FOR PNCs
ex_s = 440
ex_e = 460

####### Blank Excitation Integral
blk_exc_int = hp.integrate(blk_x, blk_y, ex_s, ex_e)

####### Dilute Excitation Integral
dil_exc_int = hp.integrate(dil_x, dil_y, ex_s, ex_e)

####### Conc Excitation Integral
conc_exc_int = hp.integrate(conc_x, conc_y, ex_s, ex_e)

####### Define Emission integration region
# # FOR COUMARIN 6
# emi_s = 460
# emi_e = 680

# FOR PNCs
emi_s = 472
emi_e = 560

# # 466 - 575
# emi_s = 466
# emi_e = 575

####### Blank Emission Integral
blk_emi_int = hp.integrate(blk_x, blk_y, emi_s, emi_e)

####### Dilute Emission Integral
dil_emi_int = hp.integrate(dil_x, dil_y, emi_s, emi_e)

####### Conc Emission Integral
conc_emi_int = hp.integrate(conc_x, conc_y, emi_s, emi_e)

####### Calculate dilute emission integral
dilute_plqy = (dil_emi_int - blk_emi_int) / (blk_exc_int - dil_exc_int)
print('dilute plqy', dilute_plqy * 100)

# observed_plqy = (conc_emi_int - blk_emi_int) / (blk_exc_int - conc_exc_int)
# print('uncorrected plqy', observed_plqy * 100)

####### Calculate PLQY after reabsorption correction
# plqy = hp.process_and_correct(dil_x, 
#                             dil_y, 
#                             conc_x, 
#                             conc_y, 
#                             observed_plqy, 
#                             emi_s=emi_s, 
#                             emi_e=emi_e, 
#                             scale_factor=1.1)
# print('corrected plqy', plqy * 100)

####### Plot the emission of the concentrated distorted and dilute scaled plots to adjust the scale_factor

# plt.title('PLQY')
# plt.ylabel('Normalized Intensity (a.u.)')
# plt.xlabel('Wavelength (nm)')
# plt.legend()
# # helper.save_fig(f'{sample} PLQY scaling factor')
# plt.show()

# Example data
# data_corrected = {
#     'Conc': ['1.3', '0.650', '0.081', '0.010'],
#     'PLQY': ['90.07%', '88.43%', '68.85%', '42.45%']
# }

# data_uncorrected = {
#     'Conc': ['1.3', '0.650', '0.081', '0.010'],
#     'PLQY': ['81.44%', '83.14%', '66.77%', '43.44%']
# }

# Call the function to plot

# hp.plot_scatter_with_lines(data_corrected, title=f'PLQY Concentration Dependance')
# # hp.plot_scatter_with_lines(data_uncorrected, title=f'{sample} PLQY Concentration Study', label='PLQY Uncorrected', color='red')
# plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# helper.save_fig(f'{sample} PLQY Concentration Study')
# plt.show()
