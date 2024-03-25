import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema
from scipy import integrate

alphabet = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
numbers = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 1 8 19 20 21 22 23 24 25 26'.split()

def normalize(y: pd.core.series.Series, x: pd.core.series.Series = None, x_num: int = None) -> pd.core.series.Series:
    if x_num is None:
        normailzed = y / np.max(y)
        return normailzed
    elif x_num and x is not None:
        i = 0
        while x[i] < x_num: i += 1
        normailzed = y / y[i]
        return normailzed

def normNthPeak(series: pd.core.series.Series, 
                series2: pd.core.series.Series, 
                nth: int = 1, 
                plot: bool= False, 
                label:str = None, 
                threshold: float = 0.01, 
                plotMax: bool = False,
                fill: bool = False,
                integral: bool = False):
    """
    Normalizes the `nth` highest peak in `series2` with the option to plot the graph and max point.

    Args:
    -
        `series`: The array for x values.

        `series2`: The array for y values whose `nth` highest peak will be determined.

        `nth`: The value for the `nth` highest peak.

        `plot`: Boolean value for displaying the plot.

    Returns:
    -
        A new `x` and `y` array that contains the `nth` highest normalized peak and the index `i` associated with the `nth` peak.
    
    Optionally Returns:
    -
        If `plot` set to `True`, then optionally returns a matplotlib plot for the `nth` highest peak point.
    """
    x, y, i = nthPeakPlotter(series, series2, nth=nth, threshold=threshold)
    y = y / np.max(y)
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    suf = suffixes.get(nth, 'th')

    if plot == True:
        if label is not None:
            label = label
        else:
            label = f'{nth}{suf} Peak'        
        plt.plot(x, y, label=label)
        if plotMax == True:
            plt.plot(x[i], y[i], marker='o', markerfacecolor='black', label='Max ' + format_float(x[i], 1) + ' nm')
        if fill == True:
            integral = integrate.trapezoid(y, x)
            plt.fill_between(x, y, alpha=0.3)
            return x, y, integral
    if integral == True:
        integral = integrate.trapezoid(y, x)
        return x, y, integral
    return x, y

def format_float(num:float, dec:int =1) -> str:
    float_formatter = "{:.{}f}".format
    formatted = float_formatter(num, dec)
    return formatted

# Absorbance/Photoluminesence Axes/title graphing function
def AP_AxesNames(samp_name: str):
    title = samp_name
    x_label = 'Wavelength (nm)'
    y_label = 'Normalized Intensity (a.u.)'
    return plt.xlabel(x_label), plt.ylabel(y_label), plt.title(title)

# Absorbance/Photoluminesence Axes/title graphing function
def XRD_AxesNames(samp_name: str):
    title = samp_name + ' XRD'
    x_label = '2'r'$\theta$ (degree)'
    y_label = 'Intensity (a.u.)'
    return plt.xlabel(x_label), plt.ylabel(y_label), plt.title(title)

def avg(x: pd.core.series.Series, y: pd.core.series.Series, xmin: float, xmax: float):
    i = 0
    k = 0
    while x[i] <= xmin: i += 1
    while x[k] <= xmax: k += 1
    avg = np.average(y[i:k])
    return avg

def baseline(series: pd.core.series.Series, threshold: int = 0.01) -> float:
    series = np.array(series)
    max = np.max(series)
    # newX = series[series <= max * threshold]
    newX = series[series <= (max * threshold)]
    avg = np.average(newX)
    return avg

def basePointsIdx(x: pd.core.series.Series, y:pd.core.series.Series, nthPeak: int = 1) -> float:

    base = baseline(y)
    max, i = nthMax(y, nthPeak)
    l_idx = i
    r_idx = i
    while y[l_idx] > base: l_idx -= 1
    while y[r_idx] > base: r_idx += 1
    lx = x[l_idx]
    ly = y[l_idx]
    rx = x[r_idx]
    ry = y[r_idx]
    return l_idx, r_idx

def basePoints(x: pd.core.series.Series, y:pd.core.series.Series, nthPeak: int = 1) -> float:

    base = baseline(y)
    max, i = nthMax(y, nthPeak)
    l_idx = i
    r_idx = i
    while y[l_idx] > base: l_idx -= 1
    while y[r_idx] > base: r_idx += 1
    lx = x[l_idx]
    ly = y[l_idx]
    rx = x[r_idx]
    ry = y[r_idx]
    return lx, ly, rx, ry

def nthPeakPicker(series: pd.core.series.Series, series2: pd.core.series.Series, nth: int = 1):
    base = baseline(series2, 0.01)
    max_idx, maxVal = localMaxima(series2, nth)
    l_idx = max_idx
    r_idx = max_idx

    while l_idx > 0 and series2[l_idx] > base: l_idx -= 1
    while r_idx < len(series2) - 1 and series2[r_idx] > base: r_idx += 1  

    series = series[l_idx:r_idx]
    series2 = series2[l_idx:r_idx]

    x = np.array(series)
    y = np.array(series2)
    return x, y

def integralPlotter (series: pd.core.series.Series, series2: pd.core.series.Series, label: str, alpha: float):
    return plt.plot(series, series2, label=label), plt.fill_between(series, series2, alpha=alpha)

############################## nth Peak Plotter ##############################

def nthPeakPlotter(series: pd.core.series.Series, 
                series2: pd.core.series.Series, 
                nth: int = 1, 
                plot: bool= False, 
                label:str = None, 
                threshold: float = 0.1, 
                plotMax: bool = False,
                fill: bool = False,
                integral: bool = False,
                scale: int = None):
    """
    Retrieve's the `nth` highest peak array and point of a given array, optionally plotting the point.

    Args:
    -
        `series`: The array for x values.

        `series2`: The array for y values whose highest peak will be determined.

        `nth`: The value for the `nth` highest peak.

        `plot`: Boolean value for displaying the plot.

    Returns:
    -
        A new `x` and `y` array that contains the `nth` highest peak and the index `i` associated with the `nth` peak.
    
    Optionally Returns:
    -
        If `plot` set to `True`, then optionally returns a matplotlib plot for the `nth` highest peak point.
    """
    base = baseline(series2, threshold=threshold)
    i, val = localMaxima(series2, nth)
    l_idx = i
    r_idx = i

    while l_idx > 0 and series2[l_idx] > base: l_idx -= 1
    while r_idx < len(series2) - 1 and series2[r_idx] > base: r_idx += 1  

    series = series[l_idx:r_idx]
    series2 = series2[l_idx:r_idx]

    i = i - l_idx
    x = np.array(series)
    y = np.array(series2)
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    suf = suffixes.get(nth, 'th')

    if scale is not None:
        y = (y / np.max(y)) * scale

    if plot == True:
        if label is not None:
            label = label
        else:
            label = f'{nth}{suf} Peak'        
        plt.plot(x, y, label=label)

        if plotMax == True:
            plt.plot(x[i], y[i], marker='o', markerfacecolor='black', label='Max ' + format_float(x[i], 1) + ' nm')
        if fill == True:
            integral = integrate.trapezoid(y, x)
            plt.fill_between(x, y, alpha=0.1)
            return x, y, integral
    if integral == True:
        integral = integrate.trapezoid(y, x)
        return x, y, integral
    return x, y, i

# Used in nthPlotPicker
def localMaxima(series, nth:int =1):
    x = np.array(series)

    loc_max_idxs = argrelextrema(x, np.greater)[0]
    loc_max_vals = x[loc_max_idxs]

    if len(loc_max_idxs) < nth:
        print(f"There are not enough local maxima in the series to retrieve the {nth}th highest local maximum.")
        return None

    # Sort local maxima values in descending order
    sorted_max_idxs = np.argsort(loc_max_vals)[::-1]
    sorted_max_vals = loc_max_vals[sorted_max_idxs]

    # Select the nth highest peak
    nth_max_idx = loc_max_idxs[sorted_max_idxs[nth - 1]]
    nth_max_val = sorted_max_vals[nth - 1]

    return nth_max_idx, nth_max_val

def plotlocalMaxima(series, nth:int =1):
    x = np.array(series)

    local_maxima_indices = argrelextrema(x, np.greater)[0]
    local_maxima_values = x[local_maxima_indices]

    if len(local_maxima_indices) < nth:
        print(f"There are not enough local maxima in the series to retrieve the {nth}th highest local maximum.")
        return None

    # Sort local maxima values in descending order
    sorted_maxima_indices = np.argsort(local_maxima_values)[::-1]
    sorted_maxima_values = local_maxima_values[sorted_maxima_indices]

    # Select the nth highest peak
    nth_maxima_index = local_maxima_indices[sorted_maxima_indices[nth - 1]]
    nth_maxima_value = sorted_maxima_values[nth - 1]

    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    suf = suffixes.get(nth, 'th')

    # Plot the series
    plt.plot(x, label='Series')
    plt.plot(nth_maxima_index, nth_maxima_value, marker='o', markerfacecolor='black', label=f'{nth}{suf} Peak')
    # Plot only the nth highest peak
    # plt.plot(nth_maxima_index, nth_maxima_value, 'ro', label=f'{nth} Peak')

    # plt.xlabel('Index')
    # plt.ylabel('Value')
    # plt.legend()
    # plt.show()

    return None

def getMaxPoint(series1: pd.core.series.Series, series2: pd.core.series.Series, min_x: int, max_x: int) -> float:
    # Getting the index who's value is equal to min_x
    min_idx = 0
    while series1[min_idx] < min_x: min_idx += 1

    # Getting the index who's value is equal to max_x
    max_idx = 0
    while series1[max_idx] < max_x: max_idx += 1

    # Creating a new series with the new min and max indexes
    series_y = series2[min_idx:max_idx]

    x = series1[series_y.argmax(axis=0)+min_idx]
    y = np.max(series_y)
    return x, y 

def plotMaxPoint(series1: pd.core.series.Series, series2: pd.core.series.Series, min_x: int, max_x: int):
    
    # Getting the index who's value is equal to min_x
    min_idx = 0
    while series1[min_idx] < min_x: min_idx += 1

    # Getting the index who's value is equal to max_x
    max_idx = 0
    while series1[max_idx] < max_x: max_idx += 1

    # Creating a new series with the new min and max indexes
    series_y = series2[min_idx:max_idx]

    x = series1[series_y.argmax(axis=0)+min_idx]
    y = np.max(series_y)
    float_formatter = "{:.1f}".format
    # print('lower bound')
    # print(min_idx)
    # print('upper bound')
    # print(max_idx)
    return plt.plot(x, y, marker='o', markerfacecolor='black', 
         label='Max ' + str(float_formatter(x)) + ' nm')

def index(series1: pd.core.series.Series, x: int):
    try:
        # Getting the index whose value is equal to x
        idx = 0
        while series1[idx] < x:
            idx += 1
        return idx
    except IndexError:
        return np.argmax(series1)

def nthMax(series: pd.core.series.Series, nth: int = 1) -> int:
    sorted = np.sort(series)[::-1]
    max = sorted[nth-1]
    i = 0
    while series[i] < max: i += 1
    return max, i

def fwhm(pl_wave: pd.core.series.Series, pl_int: pd.core.series.Series):

    pl_norm_inten = pl_int / np.max(pl_int)
    x_eV = 1239.84 / pl_wave
    y_eV = pl_int * (1239.84/pl_wave)**2

    #Identify peak
    max_idx = y_eV.argmax(axis=0)
    half_max_int = (y_eV[max_idx] / 2) + 1000

    hf_mx_int = pl_norm_inten[max_idx] / 2

    # Identifying the lower and upper indexes for the PL peak
    min_idx = max_idx
    while y_eV[min_idx] > half_max_int: min_idx -=1
    while y_eV[max_idx] > half_max_int: max_idx += 1

    # Full Width at Half Max value
    fwhm = (x_eV[min_idx] - x_eV[max_idx]) * 1000

    # Visual Plost of the FWHM
    hm_x = np.linspace(pl_wave[min_idx],pl_wave[max_idx],100)
    hm_y = np.linspace(hf_mx_int,hf_mx_int,100)

    return plt.plot(hm_x,hm_y, label=str('FWHM = {:.1f}'.format(fwhm)) + ' meV')

def ssdat2txt(paths: list[str]) -> list[np.ndarray]:
    paths = paths.split()

    x_list = []
    y_list = []

    for path in paths:
        # Read the file
        with open(path, 'r') as file:
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
            if is_floatable(line[0]):
                clean_data.append(line)

        df = pd.DataFrame(clean_data, columns=['Wavelength', 'Intensity'])

        # Assuming you have already created the DataFrame df
        x = df['Wavelength']
        y = df['Intensity']

        # Assuming df is your DataFrame containing the 'Wavelength' and 'Intensity' columns
        x = pd.to_numeric(df['Wavelength'], errors='coerce')
        y = pd.to_numeric(df['Intensity'], errors='coerce')
        
        x_list.append(x)
        y_list.append(y)

    return np.array(x_list), np.array(y_list)
