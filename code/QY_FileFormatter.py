import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the file
with open('/Users/josuehernandez/Downloads/drive-download-20230619T201203Z-001/A_JH12_5TO7A.txt', 'r') as file:
    lines = file.readlines()

# Find the starting index of the data
start_index = lines.index("Wavelength (nm)()\tSignal (V)()\tDetector Index (#)()\tGrating Index (#)()\tFilter Index (#)()\n") + 1

# Extract the data lines
data_lines = [line.strip().split()[:2] for line in lines[start_index:]]

def is_floatable(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# for line in data_lines:
clean_data = []
for line in data_lines:
    for i in np.arange(2):
        if is_floatable(line[i]):
            # print(line[i])
            clean_data.append(line)
# print(data)

# Convert the data to a DataFrame
df = pd.DataFrame(clean_data)

# Save the processed data to a new file
df.to_csv("processed_data_NEW.csv", index=False)

data = pd.read_csv('processed_data_NEW.csv', delimiter=',', names=('wavelength', 'intensity'))

x = data.wavelength
y = data.intensity

plt.plot(x, y)
plt.show()
