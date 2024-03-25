import matplotlib.pyplot as plt
import pandas as pd

j=0
ftir_paths = '''
/Users/josuehernandez/Downloads/CsOA_Old.txt
/Users/josuehernandez/Downloads/CsOA.txt
'''.split()
samp_ID = '''
Old CsOA
New CsOA
'''.split()

for path in ftir_paths:
    ftir_Data = pd.read_csv(path, names=('wavenumber', 'intensity'))

    ################################### Abs Data ###################################
    ftir_x = ftir_Data.wavenumber
    ftir_y = ftir_Data.intensity

    ################################### Plots ###################################
    # Plot Abs & PL
    plt.plot(ftir_x, ftir_y, label='Abs ' + ' ' + samp_ID[j])
    # plt.plot(plX, plYNorm, 'r', label='PL ' + saveName)
    # plt.plot(plX, plYNorm, label='PL ' + ' ' + sampID[j])

    plt.title('Old vs New CsOA FTIR')
    # plt.xlim([300, 750])
    # plt.ylim([0, absYNorm[idx] + 0.02])
    plt.legend()
    # plt.savefig(savePath, dpi=1200)
    j+=1
plt.show()
