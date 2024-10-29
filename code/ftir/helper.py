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
        # the delimiter of the data in csv is a comma so this needs to be a comma
        split_line = line.split(',')
        # print(element for element in split_line)
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
