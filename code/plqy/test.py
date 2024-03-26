import numpy as np
from scipy.interpolate import pchip_interpolate

# Example data points
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])

# Define points for interpolation
x_interp = np.linspace(0, 4, 100)

# Perform PCHIP interpolation
y_interp = pchip_interpolate(x, y, x_interp)

# Plot the original data and the interpolated curve
import matplotlib.pyplot as plt
plt.plot(x, y, 'ro', label='Original Data')
plt.plot(x_interp, y_interp, label='Interpolated Curve')
plt.xlabel('x')
plt.ylabel('y')
plt.title('PCHIP Interpolation')
plt.legend()
plt.grid(True)
plt.show()
