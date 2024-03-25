from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import sys
import helper as h

# Check if additional parameter is provided
if len(sys.argv) > 1:
    try:
        value = int(sys.argv[1])  # Convert the argument to an integer
    except ValueError:
        value = 300
        print(f"Invalid parameter. Parameter must be an integer. Using default value of {value}.")
else:
    value = 300
    print(f"Using default value of {value}")

abs_paths = '''
/Users/josuehernandez/jh_sheldon_group/data/Abs/jh_samples/crude/Abs_JH4.txt
'''.split()

pl_paths = '''
/Users/josuehernandez/jh_sheldon_group/data/PL/crude/PL_JH4.txt
'''.split()

if len(abs_paths) != len(pl_paths): 
    print('Make sure you have equal number of absorbance and photoluminescence files')
    print('Abs_paths', abs_paths)
    print('Pl_paths', pl_paths)
else:
    for i in np.arange(len(abs_paths)):
        abs_path = abs_paths[i]
        pl_path = pl_paths[i]

        abs_data = pd.read_csv(abs_path, delimiter=h.delimiter(abs_path), names=(['wavelength', 'intensity']))
        pl_data = pd.read_csv(pl_path, delimiter=h.delimiter(pl_path), names=(['wavelength', 'intensity']))

        abs_wavelength = abs_data.wavelength
        abs_intensity, abs_intensity_idx = h.norm(abs_data.intensity, abs_wavelength, value)

        pl_wavelength = pl_data.wavelength
        pl_intensity = h.norm(pl_data.intensity)

        plt.plot(abs_wavelength, abs_intensity, label='Abs')
        plt.plot(pl_wavelength, pl_intensity, label='PL')


        plt.xlim([value, 700])
        plt.ylim([0, 1])
        plt.title('Absorbance and Photoluminescence Plot')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity (a.u.)')
        plt.legend()
plt.show()
