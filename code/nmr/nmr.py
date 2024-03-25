import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
import os

# Specify the relative path to the directory
relative_path = '/Users/josuehernandez/Downloads/NMR Files/RAW/JH_OA_CDCl3_103123/20'

# Convert to absolute path
nmr_file_path = os.path.abspath(relative_path)

# Check if the directory exists
if os.path.exists(nmr_file_path):
    # Load the NMR data
    dic, data = ng.bruker.read(nmr_file_path)

    # Extract data from 'acqus' and 'procs' dictionaries
    acqus = dic['acqus']
    procs = dic['procs']

    # Perform Fourier transform on the data
    ft_data = ng.proc_base.fft(data)

    # Calculate the spectral width considering half of 'procs['SI']'
    spectral_width = procs['SI'] / (2 * acqus['BF1'])
    offset = procs['OFFSET']

    # Generate the chemical shift axis with half the number of points
    chemical_shift_axis = np.linspace(offset + spectral_width / 2, offset - spectral_width / 2, len(ft_data))

    # Calculate the power spectral density
    power_spectral_density = (np.abs(ft_data) ** 2) / (spectral_width * len(ft_data))

    # Reverse both arrays to mirror the data
    chemical_shift_axis = chemical_shift_axis[::-1]
    power_spectral_density = power_spectral_density[::-1]

    # Create the NMR plot
    plt.figure(figsize=(10, 5))
    plt.plot(chemical_shift_axis, power_spectral_density, color='b', linewidth=1)
    plt.xlabel('Chemical Shift (ppm)')
    plt.ylabel('Power Spectral Density')
    plt.title('NMR Power Spectral Density (Mirrored)')
    plt.grid(True)
    plt.show()
else:
    print("NMR data directory not found.")
