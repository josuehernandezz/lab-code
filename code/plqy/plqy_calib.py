from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import helper as h
import temp_helper as th

save_name = 'calib_plot'
save_path = '/Users/josuehernandez/Downloads/' + save_name

# Calibration Data paths
calib_paths = '''
/Users/josuehernandez/Downloads/Correction.txt
'''.split()

# calib_paths = '''
# /Users/josuehernandez/Downloads/new_Correction.txt
# '''.split()

for i in np.arange(len(calib_paths)):
    calib_path = calib_paths[i]

    calib_data = th.path2df(calib_path)
    calib_data = h.path2df(calib_path)

    x = calib_data.iloc[:, 0]
    y = calib_data.iloc[:, 1]

    plt.plot(x,y, label='Old Calibration ' + str(i+1))

    plt.xlim([350, 1000])
    plt.title('PLQY Calibration')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend()
    # plt.savefig(save_path, dpi=1200)
plt.show()
