import pandas as pd

def path2df(path:str):
    lines = grab_lines_path(path)
    nums = grab_nums(lines)
    df = nums2df(nums)
    return df

def grab_lines_path(path: str):
    with open(path, 'r') as file:
        lines = file.readlines()
        return lines

def grab_nums(lines: list):
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
    try:
        float(value)
        return True
    except ValueError:
        return False
