import matplotlib.pyplot as plt
from data_helper import path2df

title = 'JLC Photoluminescence'
save_path = f'/Users/josuehernandez/Downloads/{title}'
# File paths for life time data
lt_paths = '''
/Users/josuehernandez/Downloads/jlc_32_2_emission_spectrum.dat
/Users/josuehernandez/Downloads/jlc_33_2_emission_spectrum.dat
'''.split()

lt_legend_labels = '''
jlc_32
jlc_33
'''.split()

for i, path in enumerate(lt_paths):
    # Get the data from the file path and create two columns called wavelength and intensity
    lt_data = path2df(path)
    print(lt_data)
    lt_wavelength = lt_data.column_1 / 10**-9
    lt_count = lt_data.column_2

    # lt_count_norm = (lt_count / (np.max(lt_count)))

    plt.plot(lt_wavelength, lt_count, label=lt_legend_labels[i])

plt.title(title)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (counts)')
plt.legend()
plt.savefig(save_path, dpi=1200)
plt.show()
