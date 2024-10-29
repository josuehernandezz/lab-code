from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Custom
import helper as h
import temp_helper as th

# Data paths
# dir = '/Users/josuehernandez/Downloads/6.10.24/'

path = '''
/Users/josuehernandez/jh_sheldon_group/data/IntegratingSphere/2024/6.24/6.13.24/Data/Conc-1_0TO2A
'''.splitlines()

title = 'Conc Averages'
caption=''
label = '''

'''.splitlines()
# PDA100A2 NO-Exit
label = label[1:]
for index, sample in enumerate(path[1:]):

    # Get data from file
    d = h.path2df(sample)
    wavelength = d.iloc[:,0]
    intensity = d.iloc[:,1]

    ######################## Integrating Sphere ########################
    # Plot of integrating sphere data from detectors
    # i = h.index(wavelength, 598)

    # plt.plot(wavelength[0:i], intensity[0:i], label=label[index])
    plt.plot(wavelength, intensity, label=label[index])

    plt.title(title)
    plt.ylabel('Intensity (V)')
    plt.xlabel('Wavelength (nm)')
    # plt.xlim([350, 600])
    plt.ticklabel_format(style='sci', axis='y', scilimits=(-3,3))
    # plt.legend()
    
######################## Figure Caption ########################    

    # plt.figtext(0.5, 0.05, caption, wrap=True, horizontalalignment='center', fontsize=12)
    # plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin


######################## Figure file Save ########################
save_fig_path = '/Users/josuehernandez/Downloads/figs/6.16.24-Clibration_QY_data/' + title
plt.savefig(save_fig_path, dpi=1200) # Save Figure

plt.show()

# grab the last item in the file path (name of the file) and clean up
# file_name = sample.split('/')[-1]
# clean_file_name = ' '.join(file_name.split('-')[3:]) 
# label = ' '.join(clean_file_name.split('.')[:-1])
    
# Create a new figure for each plot
# plt.figure()
