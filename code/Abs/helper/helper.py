def detDelim(path):
    '''
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
