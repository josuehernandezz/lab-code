import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate

############################## Files: Corretion, Blank, True (Diluted), Observed (Undiluted) ##############################
corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_i.txt'
# corr_path = '/Users/josuehernandez/Library/Mobile Documents/com~apple~CloudDocs/Sheldon Group/SLS Project/2025_correction_inverted.txt'
############################## Importing ##############################
cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))

cor_x = cor.wavelength
cor_y = cor.voltage

plt.plot(cor_x, cor_y)
plt.show()
