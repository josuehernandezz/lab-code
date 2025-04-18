import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def delimiter(path:str):
    '''
    Returns the delimiter of a file

    Args
    -
        `path` the filepath of the file

    Delimiters
    -
        r`tab \t`, `space`, `comma ,`, `semicolon ;`
    '''
    with open(path) as file:
        first_line = file.readline().strip()
        delimiters = ['\t', ' ', ',', ';']

    for delimiter in delimiters:
        if delimiter in first_line:
            return delimiter
        else:
            return print('Delimiter not found.')
    return None

def norm(y, x = None, num: int = None):
    '''
    This function normalizes an array `y` to either of the following: the `y` array's maximum value, or
    optionally, to a specific value `num` in the `x` array.
    
    Args:
    -
        `y` the array of values that will be normalized.
    
        `x` the array of values that is used in normalizing the `y` array at the value `num`.
        
        `num` the value that the `y` array is normalized to along the `x` array.
    '''
    if num is None:
        y = y / max(y)
        return y
    else:
        i = 0 # Normalize to N nm
        # sheldon: <, fout: >
        while x[i] < num and i < len(x): i += 1
        y = y / y[i]
        return y, i

def test(test):
    print(test)

def path2df(path:str):
    lines = grab_lines_path(path)
    nums = grab_nums(lines)
    df = nums2df(nums)
    return df

def file2df(file):
    '''
    Takes a file and extracts the lines with numbers and returns a panda data frame with two columns
    '''
    try:
        lines = grab_lines_file(file)
        data = grab_nums(lines)
        df = nums2df(data)
        return df
    except Exception:
        try:
            df = pd.read_csv(file, delimiter=delimiter(file), names=['wavelength', 'intensity'])
            return df
        except Exception as e:
            print(f"Error processing file in file2df: {file}")
            print(f"Error message in file2df: {str(e)}")

def grab_lines_path(path: str):
    with open(path, 'r') as file:
        lines = file.readlines()
        return lines

def grab_lines_file(file) -> list:
    '''
    Takes fine, and separates data into lines.

    '''
    file.seek(0)    
    lines = [line.decode() for line in file.readlines()]
    print('lines', lines)
    return lines

def grab_nums(lines: list):
    '''
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

def index(series1: pd.core.series.Series, x: int):
    '''
    This function takes in a function and a wavelength as input, and scans through the function
    until it grabs the index of the wavelength just below the input wavelength.    
    '''
    try:
        # Getting the index whose value is equal to x
        idx = 0
        while series1[idx] < x:
            idx += 1
        return idx
    except IndexError:
        return np.argmax(series1)

def plot2txt(x, y, file_name:str, path:str = None,):
    data = np.column_stack((x, y))
    if path == None:
        save_txt_path = '/Users/josuehernandez/Downloads/' + file_name + '.txt'
    else:
        save_txt_path = path + file_name
    return np.savetxt(save_txt_path, data, delimiter=',') # Save text file

def save_fig(fig_name:str, path:str = None):
    '''
    Takes a file name and saves the figure to the downloads folder.
    '''
    if path == None:
        save_fig_path = '/Users/josuehernandez/Downloads/' + fig_name + '.png'
    else:
        save_fig_path = path + fig_name
    return plt.savefig(save_fig_path, dpi=1200) # Save Figure
