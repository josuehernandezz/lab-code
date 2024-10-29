import matplotlib.pyplot as plt
import pandas as pd
import helper as hp

sample = "Cesium Oleate"
ftir_path = "/Users/josuehernandez/Downloads/drive-download-20241021T210026Z-001/cesium_oleate_raw.csv"
fitr_path3 = "/Users/josuehernandez/Downloads/drive-download-20241021T210026Z-001/cesium_oleate_corrected.csv"
ftir_path2 = "/Users/josuehernandez/Downloads/drive-download-20241021T205444Z-001/oleic_acid_corrected.csv"
# ftir_path3 = "/Users/josuehernandez/Downloads/drive-download-20241021T204439Z-001/lead_oleate_corrected_run2.csv"

ftir_data = hp.path2df(ftir_path)
ftir_data2 = hp.path2df(ftir_path2)
ftir_data3 = hp.path2df(fitr_path3)

wavenumber = ftir_data.column_1
transmittance = ftir_data.column_2

wavenumber2 = ftir_data2.column_1
transmittance2 = ftir_data2.column_2

wavenumber3 = ftir_data3.column_1
transmittance3 = ftir_data3.column_2

# plt.plot(wavenumber, transmittance, label='Raw')
plt.plot(wavenumber2, transmittance2, label='OA')
plt.plot(wavenumber3, transmittance3, label='CsOA')
plt.gca().invert_xaxis()
# plt.gca().invert_yaxis()

plt.xlim([4000, 1200])

plt.title(f'{sample} IR Spectra')
plt.ylabel('% Transmittance')
plt.xlabel('wavenumber (1/cm)')
plt.legend()

folder = "/Users/josuehernandez/Downloads/"

save_path = folder + sample + ".png"
plt.savefig(save_path, dpi=1200)

plt.show()
