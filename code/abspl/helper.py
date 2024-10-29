
def delimiter(path:str):
    r'''
    Description:
    -
    Returns the delimiter of a file.

    Args
    -
        `path` the filepath of the file.

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

def norm(y, x = None, num: int = None):
    r'''
    Description:
    -
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

def index(series, wavelength):
    r'''
    Description:
    -
    Takes in a series of data and a wavelength value, and will return the index of the closest wavelength.
    '''
    i = 0
    while series[i] <= wavelength:
        i+=1
    return i

def calculate_absorbance(abs_wavelength, abs_intensity, wavelength = 335):
    r'''
    Description:
    -
    Gets the absorbance at 335nm to determine NC concentration

    Args:
    -
        `abs_wavelength` : The data series that is used to get the index at the wavelength, default is 335nm

        `abs_intensity` : The data series that is used to get the intensity value from the index calculated

        Optional:
        -
            `wavelength` : The wavelength get the absorbance from.
    '''
    i_at_wavelength = index(abs_wavelength, wavelength)
    abs_at_wavelength = abs_intensity[i_at_wavelength]
    return abs_at_wavelength

def calculate_concentration(absorbance, abs_intensity, b = 8.32) -> float:
    r'''
    Description:
    -
    Calculates the concentration of the nanocrystals given the absorbance value at the relevant wavelength
    (335 for perovskite NCs) and the absorbance intensity data series.

    Uses the Beer-Lambert Law where:
        A = ε * c * l

        A = absorbance

        ε = molar absorptivity
        
        c = concentration
        
        l = length

    Args:
    - 

        `absorbance` : The absorbance value that was measured at the wavelength. This will depend on the specific sample.
        In the case of CsPbBr3 nanocrystals the absorbance value is measured at 335nm.

        `abs_intensity` : The data series that is used in order to determine the maximum photoluminescence value.

    PL will have an approximate cude edge length of:
    
    8.2 nm λ = 508 nm

    8.32 nm λ = 510 nm

    8.5 nm λ = 512 nm
    '''

    pl = max(abs_intensity)
    ε = 0.052 * (b ** 3)
    c = absorbance / (b * ε)
    return c

# M1V1 = M2V2
# M1 = starting conc.
# V1 = 50 uL
# M2 = c
# V2 = Final Volume of NCs (2mL + 50uL + 3mL + 2mL + 1mL)
