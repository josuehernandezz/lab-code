import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import gaussian_filter1d
# custom
import helper as h

def spline(data_x, data_y_norm, s=0.05):
    # Fit a spline to the data
    spline = UnivariateSpline(data_x, data_y_norm, s=s)  # 's' controls the smoothing factor
    
    x_smooth = np.linspace(data_x.min(), data_x.max(), 100)
    y_smooth = spline(x_smooth) / np.max(spline(x_smooth))
    return plt.plot(x_smooth, y_smooth, label=names[i]+' spline')

sample = 'EB07'

def gaussian(data_x, data_y_norm, sigma):
    y_smooth = gaussian_filter1d(data_y_norm, sigma=sigma)
    y_smooth = y_smooth / np.max(y_smooth)
    return plt.plot(data_x, y_smooth, label=names[i])

# PLQY file paths
paths = [
'/Users/josuehernandez/Downloads/Data 2/dilute_1_stock_000.ssdat', 
    '/Users/josuehernandez/Downloads/Data 2/dilute_2_1mLstock_1mLHex_000.ssdat', 
    '/Users/josuehernandez/Downloads/Data 2/dilute_3_250uL_2mL_000.ssdat', 
    '/Users/josuehernandez/Downloads/Data 2/dilute_4_250uL_2mL_000.ssdat'
    ]

names = ['1.3 µM', '0.650 µM', '0.081 µM', '0.010 µM']

emi_s = 472
emi_e = 570

for i, path in enumerate(paths):
    data = h.path2df(path)

    emi_s_i = h.index(data.column_1, emi_s)
    emi_e_i = h.index(data.column_1, emi_e)
    data_x = data.column_1[emi_s_i:emi_e_i]
    data_y = data.column_2[emi_s_i:emi_e_i]
    
    data_y_norm = data_y / np.max(data_y)

    # spline(data_x, data_y_norm, s=0.05)
    # plt.plot(data_x, data_y_norm, label=names[i])
    gaussian(data_x, data_y_norm, 2)
    plt.title('EB07 Reabsorption Redshift')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Normalized Intensity (a.u.)')
    plt.xlim([480, 560])
    plt.ylim([0, 1.02])
    plt.legend()

h.save_fig('EB07_reabsorption_shifts')
plt.show()
