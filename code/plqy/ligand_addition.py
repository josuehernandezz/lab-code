from matplotlib import pyplot as plt
import numpy as np

import helper as h

sample_name = 'MM04'

ligand_conc = np.array([0, 2, 6, 10])
plqy_data = np.array([42.45, 91.18, 107.83, 103.8]) / 100
errors = np.array([0.07] * len(plqy_data))  # Assuming uniform error

# Texas A&M Maroon
tamu_maroon = '#500000'

# Plot the line separately in blue
plt.plot(ligand_conc, plqy_data, color='red', linestyle='-')

# Plot error bars with red markers, no connecting line
plt.errorbar(
    ligand_conc,
    plqy_data,
    yerr=errors,
    fmt='o',
    markerfacecolor='blue',
    markeredgecolor='blue',
    linestyle='none',
    ecolor='red',
    capsize=5,
    label='PLQY'
)

plt.xlabel('1:1 OA:OAm Concentration (mM)')
plt.ylabel('Absolute PLQY')
plt.title(f'{sample_name} 1:1 Ligand Addition Study')
plt.xlim([-0.1, 10.1])
plt.legend()

h.save_fig(f'{sample_name}_ligand_addition_study')

plt.show()
