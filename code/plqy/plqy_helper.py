import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.integrate import trapezoid

def path2df(path:str):
    lines = grab_lines_path(path)
    nums = grab_nums(lines)
    df = nums2df(nums)
    return df

def grab_lines_path(path: str):
    with open(path, 'r') as file:
        return file.readlines()
    
def grab_nums(lines: list):
    r'''
    Takes a list of lines, and tests items in each line that are convertable to a float, 
    
    if any item in line is not convertable, the line is discarded.
    
    '''
    nums = []
    for line in lines:
        split_line = line.split()
        if split_line and all(is_float(element) for element in split_line):
            nums.append([float(element) for element in split_line])
    return nums

def nums2df(nums: list[float]) -> pd.DataFrame:
    column_names = [ f'column_{i+1}' for i, val in enumerate(nums[0])]
    df = pd.DataFrame(nums)
    df.columns = column_names
    return df

def is_float(value):
    if value == 'NaN':
        return False
    else:
        try:
            float(value)
            return True
        except ValueError:
            return False

def index(series, wavelength):
    r'''
    This function takes a `series` and a `wavelength` as an input and will return the index of the series at that
    wavelength.
    '''

    i = 0
    while wavelength >= series[i]:
        i+=1
    return i

def delimiter(path:str):
    r'''
    Returns the delimiter of a file

    Args
    -
        `path` the filepath of the file

    Delimiters
    -
        `tab \ t`, `space`, `comma ,`, `semicolon ;`
    '''
    with open(path) as file:
        first_line = file.readline().strip()
        delimiters = ['\t', ' ', ',', ';']

    for delimiter in delimiters:
        if delimiter in first_line:
            return delimiter
        else:
            return print('Delimiter not found.')

def integrate(x_series, y_series, start_nm: int, end_nm: int, plot: bool = False):
    r'''
    Description:
    -

    Calculates the integral of the `y_series` with the specified starting value `start_nm` and ending value `end_nm`.
    The integration technique that is used is the trapezoidal method from scipy.integrate.
    
    Args:
    ---
        `x_series` : The data series used to get the starting and ending indecies.
        `y_series` : The data series used to calculate the integral from.
        `start_nm` : The first point to integrate from.
        `end_nm` : The end point to integrate from.
    
    Optional Args:
    -------------
        `plot` : You can optionally make a plot of the area that is being integrated for visualization. 
        This utilizes matplotlib.pyplot. It will return a plot object.
    '''
    start_i = index(x_series, start_nm)
    end_i = index(x_series, end_nm)
    result = trapezoid(y_series[start_i:end_i], x_series[start_i:end_i])
    if plot is True:
        plt.plot(x_series[start_i:end_i], y_series[start_i:end_i])
        return result
    else:
        return result

def plot_dilute_scaled_and_conc(dil_x, dil_y, conc_x, conc_y, emi_s:int = 460, emi_e:int = 545, scale_factor:int = 1):
    '''
    Description
    -----------

    This function will first normalize both the dilute and concentrated samples. Then the `scale_factor` will 
    be used to scale the dilute sample so that the red edge of the dilute overlaps with the concentrated sample.
    '''
    # Get the index of the arrays for the given wavelengths emi_S emi_e
    emi_s_i = index(dil_x, emi_s)
    emi_e_i = index(dil_x, emi_e)

    # Shorten the original array's by those of the emission region based on the emi_s emi_e values
    dil_x_emission = dil_x[emi_s_i:emi_e_i]
    conc_x_emission = conc_x[emi_s_i:emi_e_i]

    # First normalize then scale the dilute y values
    dil_y = dil_y[emi_s_i:emi_e_i]
    dil_y_norm = (dil_y / np.max(dil_y))
    dil_y_scaled = dil_y_norm * scale_factor

    # Normalize the concentrated sample values
    conc_y = conc_y[emi_s_i:emi_e_i]
    conc_y_norm = (conc_y / np.max(conc_y))

    plt.plot(dil_x_emission, dil_y_scaled, label='Dilute & Undistorted')
    plt.plot(conc_x_emission, conc_y_norm, label='Concentrated & Distorted')

    return dil_x_emission, conc_x_emission, dil_y_scaled, conc_y_norm

def reabsorption_correction(dil_x_emission, conc_x_emission, dil_y_scaled, conc_y_norm, observed_plqy):
    dil_y_scaled_integral = trapezoid(dil_y_scaled, dil_x_emission)
    conc_y_norm_integral = trapezoid(conc_y_norm, conc_x_emission)

    a = 1 - (conc_y_norm_integral / dil_y_scaled_integral)
    print('Probability of self-absorption a:', a)

    reabsorption_corrected_plqy = observed_plqy / ((1 - a) + (a * observed_plqy))

    return reabsorption_corrected_plqy

def process_and_correct(dil_x, dil_y, conc_x, conc_y, observed_plqy, emi_s=472, emi_e=570, scale_factor=1.9):
    # Call the first function and unpack the results
    dil_x_emission, conc_x_emission, dil_y_scaled, conc_y_norm = plot_dilute_scaled_and_conc(
        dil_x, dil_y, conc_x, conc_y, emi_s=emi_s, emi_e=emi_e, scale_factor=scale_factor
    )
    
    # Call the second function using the outputs from the first
    plqy = reabsorption_correction(dil_x_emission, conc_x_emission, dil_y_scaled, conc_y_norm, observed_plqy)
    
    return plqy

def plot_scatter_with_lines(data, title='Scatter Plot', xlabel=r'CsPbBr$_3$ Concentration (µM)', ylabel='Absolute PLQY (%)', label='PLQY Corrected', color='blue'):
    # Split the data into two lists for plotting
    concentrations = [float(item[:-1]) for item in data['Conc']]  # Convert from string to float, stripping '%'
    plqy_values = [float(item[:-1]) for item in data['PLQY']]    # Convert from string to float, stripping '%'

    # Create the scatter plot with lines
    plt.plot(concentrations, plqy_values, color='black', linestyle='--')  # Line color black
    plt.scatter(concentrations, plqy_values, color=color, label=label)  # Marker color blue with transparency

    # Add labels and title
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim([0, np.max(concentrations) + 0.025 * np.max(concentrations)])
    # plt.legend() 
