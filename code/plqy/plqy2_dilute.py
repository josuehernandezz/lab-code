import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid
from matplotlib.ticker import FormatStrFormatter

# import plqy_helper as hp
from . import plqy_helper as hp
import helper

sample = 'MM03'
sample_detail = sample + ' in hexane'
############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_i.txt'

blk_path = '/Volumes/Data-1/josue/IntegratingSphere/MM/MM04/Blank_hexane_000.ssdat'

dil_path = '/Volumes/Data-1/josue/IntegratingSphere/MM/MM04/MM04_in_10mM_one_to_one_000.ssdat'

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
cor_interpolation = cor_interpolation

blk_x = blk.column_1
blk_y = blk.column_2
# Apply correction factor to blank, and convert to photon counts
blk_y = blk_y * cor_interpolation * (blk_x * 10 ** -9)

dil_x = dil.column_1
dil_y = dil.column_2
# Apply correction factor to dilute sample, and convert to photon counts
dil_y = dil_y * cor_interpolation * (dil_x * 10 ** -9)

####### Define Excitation integration region

#-------unity plqy with below--------############
ex_s = 440
ex_e = 460
#---------------############

# ex_s = 440
# ex_e = 460

####### Blank Excitation Integral
blk_exc_int = hp.integrate(blk_x, blk_y, ex_s, ex_e)

####### Dilute Excitation Integral
dil_exc_int = hp.integrate(dil_x, dil_y, ex_s, ex_e)

####### Define Emission integration region

# -------unity plqy with below--------############
# emi_s = 465
# emi_e = 559
# ---------------############

emi_s = 475
emi_e = 570

# # 466 - 575
# emi_s = 466
# emi_e = 575

####### Blank Emission Integral
blk_emi_int = hp.integrate(blk_x, blk_y, emi_s, emi_e)

####### Dilute Emission Integral
dil_emi_int = hp.integrate(dil_x, dil_y, emi_s, emi_e)

####### Calculate dilute emission integral
dilute_plqy = (dil_emi_int - blk_emi_int) / (blk_exc_int - dil_exc_int)
print('Dilute plqy', dilute_plqy * 100)

# plt.plot(dil_x, dil_y)
# plt.show()
