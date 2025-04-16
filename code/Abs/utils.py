import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def index(series, wavelength):
    '''
    Description:
    -
    Takes in a series of data and a wavelength value, and will return the index of the closest wavelength.
    '''
    i = 0
    while series[i] <= wavelength:
        i+=1
    return i

def get_absorbance(abs_wavelength, abs_intensity, wavelength=335):
    """
    Description
    -----------
    Calculates the absorbance at a specified wavelength (default is 335 nm) 
    to determine the NC (nanocrystal) concentration.

    Parameters
    ----------
    abs_wavelength : array-like
        The data series containing wavelength values. This is used to find 
        the index corresponding to the specified wavelength.

    abs_intensity : array-like
        The data series containing intensity values. This is used to retrieve 
        the intensity at the index calculated from `abs_wavelength`.

    wavelength : float, optional
        The wavelength at which to calculate the absorbance. The default value 
        is 335 nm.

    Returns
    -------
    float
        The absorbance value at the specified wavelength.

    Example
    --------
    To get the absorbance at 335 nm:
    
    ```python
    absorbance = get_absorbance(abs_wavelength_data, abs_intensity_data)
    ```

    To get the absorbance at a different wavelength (e.g., 400 nm):
    
    ```python
    absorbance = get_absorbance(abs_wavelength_data, abs_intensity_data, wavelength=400)
    """
    i_at_wavelength = index(abs_wavelength, wavelength)
    abs_at_wavelength = abs_intensity[i_at_wavelength]
    return abs_at_wavelength

def calculate_concentration(absorbance, pl_intensity, pl_max_wavelength: float = 510, b: float = 8.32, **kwargs) -> float:
    """
    Description
    -----------
    Calculates the concentration of nanocrystals given the absorbance value 
    at the relevant wavelength (335 nm for perovskite NCs) and the absorbance 
    intensity data series.

    This function uses the Beer-Lambert Law, expressed as:
        A = ε * c * l

    Where:
        A = absorbance
        ε = molar absorptivity
        c = concentration
        l = length

    Parameters
    ----------
    absorbance : float
        The absorbance value measured at the wavelength. For CsPbBr3 nanocrystals, 
        this value is typically measured at 335 nm.

    pl_intensity : array-like
        The data series used to determine the maximum photoluminescence value.

    pl_max_wavelength : float
        The max peak of the photoluminescence.

    b : float, optional
        The approximate cube edge length of the nanocrystals (in nm). Default is 8.32 nm.

    Optional kwargs
    ---------------
    dilution_factor : bool
        If true the function will calculate the dilution but `v_1` and `v_2` must be supplied.
    
    v_1 : int, optional
        The volume of stock concentration added. Usually a small amount that is going to be diluted.
        For example, 50 uL diluted in 2000uL (v_1 would be 50uL)

    v_2 : int, optional
        The total volume of the solvent added plus the small amount of stock solution. For example,
        a solution made of 50 uL of stock diluted with 2000 uL of hexane would have a total volume
        of 2050 uL (v_2 would be 2050 uL)

    Returns
    -------
    float
        The calculated concentration of the nanocrystals.

    Notes
    -----
    The concentration is calculated based on the following cube edge lengths:
    - 8.2 nm for λ = 508 nm
    - 8.32 nm for λ = 510 nm
    - 8.5 nm for λ = 512 nm

    Example
    --------
    To calculate the concentration:
    
    ```python
    concentration = calculate_concentration(absorbance_value, abs_intensity_data)
    ```
    """

    dilution_factor = kwargs.pop('dilution_factor', False)
    v_1 = kwargs.pop('v_1', None)
    v_2 = kwargs.pop('v_2', None)

    # Determine the value of b based on the input wavelength
    if pl_max_wavelength < 508:
        b = 8.2
    elif pl_max_wavelength > 512:
        b = 8.5
        print("Warning: Wavelength is greater than expected; using b = 8.5 nm.")
    elif pl_max_wavelength == 510:
        b = 8.32
    else:  # wavelength is between 508 and 512 (inclusive)
        b = 8.32

    if absorbance >= 1:
        print('Cannot calculate concentration of nanocrystals at this absorbance.')
        print(f'Absorbance is greater than one: {absorbance}')
        return absorbance
    else:
        ε = 0.052 * (b ** 3) # nm^3 cm^-1 µM^-1
        c = absorbance / (ε * 1) # multiply by 1 cm

        if dilution_factor:
            concentration = "{:.2E}".format(c) + ' µM'
            stock_concentration = "{:.2}".format((c * v_2) / v_1) + ' µM'
            print(f'The dilute PNC concentration is: {concentration}')
            print(f'The stock PNC concentration is: {stock_concentration}')
            return concentration
        else:
            # Format the number in scientific notation
            concentration = "{:.2E}".format(c) + ' µM'
            print(f'The PNC concentration is: {concentration}')
            return concentration

def fwhm(pl_wave, pl_int):

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

def plotMaxPoint(x, y, min_x: int, max_x: int):
    
    # Getting the index who's value is equal to min_x
    min_idx = 0
    while x[min_idx] < min_x: min_idx += 1

    # Getting the index who's value is equal to max_x
    max_idx = 0
    while x[max_idx] < max_x: max_idx += 1

    # Creating a new series with the new min and max indexes
    series_y = y[min_idx:max_idx]

    x = x[series_y.argmax(axis=0)+min_idx]
    y = np.max(series_y)
    float_formatter = "{:.1f}".format

    return plt.plot(x, y, marker='o', markerfacecolor='black', 
         label='Max ' + str(float_formatter(x)) + ' nm')
