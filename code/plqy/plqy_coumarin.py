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

blk_path = '/Volumes/Data-1/josue/3.26.35-Full-documents-backup/IntegratingSphere/2025/1.25/1.20.25/coumarin6/blank_ethanol_000.ssdat'

dil_path = '/Volumes/Data-1/josue/3.26.35-Full-documents-backup/IntegratingSphere/2025/1.25/1.20.25/coumarin6/coumarin_6_000.ssdat'

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
dil_y = dil_y * cor_interpolation[5:] * (dil_x * 10 ** -9)

####### Define Excitation integration region

# FOR COUMARIN 6
ex_s = 395
ex_e = 415

####### Blank Excitation Integral
blk_exc_int = hp.integrate(blk_x, blk_y, ex_s, ex_e)

####### Dilute Excitation Integral
dil_exc_int = hp.integrate(dil_x, dil_y, ex_s, ex_e)

####### Define Emission integration region
# FOR COUMARIN 6
emi_s = 458
emi_e = 678

####### Blank Emission Integral
blk_emi_int = hp.integrate(blk_x, blk_y, emi_s, emi_e)

####### Dilute Emission Integral
dil_emi_int = hp.integrate(dil_x, dil_y, emi_s, emi_e)

####### Calculate dilute emission integral
coumarin_plqy = (dil_emi_int - blk_emi_int) / (blk_exc_int - dil_exc_int)
print('Coumarin plqy', coumarin_plqy * 100)
