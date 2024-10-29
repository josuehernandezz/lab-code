import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate
from scipy.integrate import trapezoid

import plqy_helper as hp

sample = 'Coumarin 6'
sample_Detail = sample + ' in Ethanol'
############################## Files: Corretion, Laser hitting empty sphere, Laser hitting sphere, Laser hitting sample  ##############################
corr_path = '/Users/josuehernandez/Downloads/correction_factor.txt'

# KL28SCN Film Measurements (Laser hitting empty sphere, Laser hitting sphere, Laser hitting sample)
empty_sphere_path = '/Users/josuehernandez/Downloads/drive-download-20241021T193838Z-001/empty_integrating_sphere_000.ssdat'
hitting_sphere_path = '/Users/josuehernandez/Downloads/drive-download-20241021T193838Z-001/KL28SCN_film_hitting_sphere_000.ssdat'
hitting_sample_path = '/Users/josuehernandez/Downloads/drive-download-20241021T193838Z-001/KL28SCN_film_hitting_sample_000.ssdat'

############################## Importing ##############################
# DELIMITER MAY BE DIFFERENT
cor = pd.read_csv(corr_path, delimiter=',', names=('wavelength', 'voltage'))
empty_sphere = hp.path2df(empty_sphere_path)
hitting_sphere = hp.path2df(hitting_sphere_path)
hitting_sample = hp.path2df(hitting_sample_path)

################### Column Selection
cor_x = cor.wavelength
cor_y = cor.voltage

# interpolates the correction data to have as many data points as the raw data (# of x data points in the blank)
cor_interpolation = pchip_interpolate(cor_x, cor_y, empty_sphere.column_1)

empty_sphere_x = empty_sphere.column_1
empty_sphere_y = empty_sphere.column_2
# Apply correction factor to empty sphere, and convert to photon counts
empty_sphere_y = empty_sphere_y * cor_interpolation * (empty_sphere_x * 10 ** -9)

hitting_sphere_x = hitting_sphere.column_1
hitting_sphere_y = hitting_sphere.column_2
# Apply correction factor to laser hitting sphere, and convert to photon counts
hitting_sphere_y = hitting_sphere_y * cor_interpolation * (hitting_sphere_x * 10 ** -9)

hitting_sample_x = hitting_sample.column_1
hitting_sample_y = hitting_sample.column_2
# Apply correction factor to laser hitting sphere, and convert to photon counts
hitting_sample_y = hitting_sample_y * cor_interpolation * (hitting_sample_x * 10 ** -9)


########################################## Define Excitation integration region
# FOR Perovskite CsPbBr3
ex_s = 440
ex_e = 460

####### Empty Sphere Excitation Integral = Le (Laser hitting empty sphere)
empty_exc_int = hp.integrate(empty_sphere_x, empty_sphere_y, ex_s, ex_e)

####### Laser hitting sphere Excitation Integral = L0 (Laser hitting sphere walls)
sphere_exc_int = hp.integrate(hitting_sphere_x, hitting_sphere_y, ex_s, ex_e)

####### Laser hitting sample Excitation Integral = Li (Laser hitting sample directly)
sample_exc_int = hp.integrate(hitting_sample_x, hitting_sample_y, ex_s, ex_e)

########################################## Define Emission integration region
# FOR PNCs
emi_s = 485
emi_e = 565

####### Laser hitting Sphere Emission Integral = E0 (Emission of secondary excitation)
sphere_emi_int = hp.integrate(hitting_sphere_x, hitting_sphere_y, emi_s, emi_e)

#######  Laser hitting sphere Emission Integral = Ei (Emission of direct excitation)
sample_emi_int = hp.integrate(hitting_sample_x, hitting_sample_y, emi_s, emi_e)

Le = empty_exc_int
L0 = sphere_exc_int
Li = sample_exc_int

E0 = sphere_emi_int
Ei = sample_emi_int

A = (L0 - Li) / L0
print('A', A)

plqy_obs = (Ei - (1 - A) * E0) / (Le * A)

print(plqy_obs * 100)

# plt.plot(blk_x, blk_y, label='blank')
# plt.plot(dil_x, dil_y, label='dilute')

# plt.title('PLQY')
# plt.ylabel('Intensity a.u.')
# plt.xlabel('Wavelength (nm)')
# plt.legend()
# plt.show()
