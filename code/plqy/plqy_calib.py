from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import helper as h
import temp_helper as th

# Calibration Data paths
calib_paths = '''
/Users/josuehernandez/Downloads/plqy_data/1_st_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/2nd_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/3rd_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/3rd_calibration_001.ssdat
/Users/josuehernandez/Downloads/plqy_data/4th_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/5th_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/6th_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/7th_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/8th_calibration_000.ssdat
/Users/josuehernandez/Downloads/plqy_data/9th_calibration_000.ssdat
'''.split()

for i in np.arange(len(calib_paths)):
    calib_path = calib_paths[i]

    calib_data = th.path2df(calib_path)
    calib_data = h.path2df(calib_path)

    x = calib_data.iloc[:, 0]
    y = calib_data.iloc[:, 1]

    plt.plot(x,y, label='Calib File ' + str(i))

    plt.xlim([350, 1000])
    plt.title('PLQY Calibration')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend()
plt.show()
