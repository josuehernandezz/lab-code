'''
Description:
-
    This library of functions is dedicated to taking on tasks related to absorbance and 
    photoluminesence plots.

'''

def norm(y, x = None, num: int = None):
    '''
    This function normalizes an array `y` to either of the following: the `y` array's maximum value, or
    optionally, to a specific value `num` in the `x` array.
    
    Args:
    -
        `y` the array of values that will be normalized.
    
        `x` the array of values that is used in normalizing the `y` array with the value `num`.
        
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
