from . import plotHelper as ph


def qyCalc(Obs_2N, En_t, Obs_2, Blk, Obs_1, dilute):
    '''
    Takes the normalized emission peak of the concentrated sample (Obs) `Obs_2N`, the enhanced emission of the 
    diluted peak `En_t`, the un-normalized emission peak of the (Obs) `Obs_2`, the blank integral `Blk`, the (Obs) excitation 
    peak `Obs_1`, and the boolean indicating the Quantum yield calculation of just the dilute sample `dilute`

    Args
    -
        `Obs_2N` Normalized observed emission integral.

        `En_t` Enhanced emission integral.
        
        `Obs_2` Observed emission integral
        
        `Blk` Blank excitation integral
        
        `Obs_1` Observed excitation integral
        
        `dilute` Boolean for calculating the quantum yield of Observed `QY`

    Returns
    -
        `Qy` The quantum yield of the sample.

    Theory
    -
        QY = (QYobs) / 1 - a

        a = 1 - int_ratio

        int_ratio = int(Normalized Undiluted Emission)/int(Enhanced diluted emission)
    '''

    a = 1 - (Obs_2N / (En_t)) # Normalized emission of Concentrated sample, divided by the diluted scaled emission such that the red tails touch.
    Qy_obs = Obs_2 / (Blk - Obs_1) # 'Normal' QY calculation. Accounting for the blank excitation
    Qy = ((Qy_obs) / ((1 - a) + (a * Qy_obs))) * 100 # QY calculation found in paper
    if dilute == True:
        Qy = Qy_obs * 100
        Qy = ph.format_float(Qy, 2) + '%'
        return Qy
    Qy = ph.format_float(Qy, 2) + '%'
    return Qy
