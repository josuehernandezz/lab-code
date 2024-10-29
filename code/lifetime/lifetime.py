import matplotlib.pyplot as plt
from data_helper import path2df

title = 'JLC Life times @620'
save_path = f'/Users/josuehernandez/Downloads/{title}'
# File paths for life time data
lt_paths = '''
/Users/josuehernandez/Downloads/jlc_32_2_lifetime_curves.dat
/Users/josuehernandez/Downloads/jlc_33_2_lifetime_curves.dat
/Users/josuehernandez/Downloads/jlc_hexane_3_component_lifetime_plot_exi_450_emi_638.dat
'''.split()

lt_names = '''
jlc_32
jlc_33
jlc_hexane_3_component
'''.split()

for i, path in enumerate(lt_paths):
    # Get the data from the file path and create two columns called wavelength and intensity
    lt_data = path2df(path)
    lt_time = lt_data.column_1 / 10**-9
    lt_count = lt_data.column_2

    # lt_count_norm = (lt_count / (np.max(lt_count)))

    plt.plot(lt_time, lt_count, label=lt_names[i])

plt.title(title)
plt.xlabel('time (ns)')
plt.ylabel('Intensity (counts)')
plt.xlim([0, 100])
# plt.ylim([0, 1])
plt.legend()
plt.savefig(save_path, dpi=1200)
plt.show()
