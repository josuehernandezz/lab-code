import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid
from matplotlib.ticker import FormatStrFormatter

# import plqy_helper as hp
from . import plqy_helper as hp
import helper as h

############################## Importing ##############################
corr_path = '/Users/josuehernandez/Downloads/2025_correction.txt'


cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))

################### Column Selection
cor_x = cor.wavelength
cor_y = cor.voltage
cor_y = 1 / cor_y


######################## Text file Save ########################

file_name = '2025_correction_i'
h.plot2txt(cor_x, cor_y, file_name)
