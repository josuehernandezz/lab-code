# function to return the save location string of our sample
def maxIndex(array: list) -> int:
    max_value = max(array)
    index = array.index(max_value)
    # print(index)
    return index
 
def APsaveLocation(folder_name: str, save_name: str) -> str:
    # add a new file name below to add that file location
    file_names = ['crude', 'fractions', 'ligands', 'powder', 'sls', 'noel_sls']
    i = 0
    while folder_name.lower() != file_names[i]:       
        if i == maxIndex(file_names)+1:
            # return print(file_names[i])
            return print('Save location not found.')
            # pass
        i += 1
    return '/Users/josuehernandez/jh_sheldon_group/figures/Abs_PL_figures/' + file_names[i] + '/' + save_name + '.png'

def XRDsaveLocation(folder_name: str, save_name: str) -> str:
    # add a new file name below to add that file location
    file_names = ['crude','sls']
    i = 0
    while folder_name.lower() != file_names[i]:
        if i == maxIndex(file_names):
            return print('Save location not found.')
        i += 1
    return '/Users/josuehernandez/jh_sheldon_group/figures/XRD_figures/' + file_names[i] + '/' + save_name + '.png'
