import csv
import json
import numpy as np


def load_json(file_path : str) -> dict:
    """
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path : string
        Path to file.

    Returns
    -------
    json file : dictionary
        .json dictionary file.

    See Also
    --------
    read_GMR_file
    save_json_dicts

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    my_dictionary = load_json(file_path="/Path/To/File")

    """
    with open(file_path, 'r') as file:
        return json.load(file)


def read_GMR_file(file_path : str) -> tuple[list, list]:
    '''
    Function Details
    ================
    Load txt output from Thorlabs spectrometer. Return wavelength in nm.

    Parameters
    ----------
    file_path: string
        Path to file.

    Returns
    -------
    wavelength, intensity: list
        Wavelength array, intensity array.

    See Also
    --------
    numpy genfromtxt

    Notes
    -----
    Returns wavelength in nm.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    08/04/2024
    ----------
    Updated documentation.

    '''
    try:
        wavelength, intensity = np.genfromtxt(
            fname=file_path,
            delimiter=';',
            unpack=True)
    except:
        wavelength, intensity = np.genfromtxt(
            fname=file_path,
            delimiter=',',
            unpack=True)
    return wavelength, intensity


def convert(o):
    """
    Check data type.

    Check type of data string.

    Parameters
    ----------
    o : string
        String to check.

    Returns
    -------
    TypeError : Boolean
        TypeError if string is not suitable.


    See Also
    --------
    None.

    Notes
    -----
    None.

    Examples
    --------
    None.

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path : str,
                    dictionary : dict) -> None:
    """
    Save .json file types.

    Use json python library to save a dictionary to a .json file.

    Parameters
    ----------
    out_path : string
        Path to file.
    dictionary : dictionary
        Dictionary to save.
    
    Returns
    -------
    None

    See Also
    --------
    load_json

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    save_json_dicts(
        out_path="/Path/To/File",
        dictionary=my_dictionary)

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')


def reflectometer_in(file_path : str) -> list:
    """
    Loads text file output from the Filmetrics spectroscopic reflectometer.

    Loads a 3 column, comma delimited, .fitnk file output from a Filmetrics F20
    spectroscopic reflectometer.

    Parameters
    ----------
    file_path: string
        Path to file.
    
    Returns
    -------
    col0, col1, col2: list
        Typically wavelength (nm), n, k.
    
    See Also
    --------
    numpy genfromtxt

    Notes
    -----
    The .fitnk file from the Filmetrics F20 contains 5 header rows and 6 footer
    rows that are seemingly not useful information. The function skips over the
    rows.

    Examples
    --------
    None

    """
    col0, col1, col2 = np.genfromtxt(
        fname=file_path,
        delimiter=',',
        skip_header=5,
        skip_footer=6,
        unpack=True)
    return col0, col1, col2


def ellipsometer_in(file_path : str) -> list:
    """
    Load text file output from the J.A. Woollam VASE.

    Loads a 5 column, comma delimited, .csv file output from a J.A. Woollam
    variable angle spectroscopic ellipsometer.

    Parameters
    ----------
    file_path: string
        Path to file.

    Returns
    -------
    col0, col1, col2, col3, col4: list
        Typically wavelength (nm), sample psi, sample delta, model psi, model
        delta.
    
    See Also
    --------
    numpy genfromtxt

    Notes
    -----
    None

    Example
    -------
    None

    """
    col0, col1, col2, col3, col4 = np.genfromtxt(
        fname=file_path,
        delimiter=',',
        skip_header=2,
        usecols=(0, 1, 2, 3, 4),
        unpack=True)
    return col0, col1, col2, col3, col4


def ellips_save(file_path : str,
                data : object) -> None:
    """
    Write n, k, epsilon real, and epsilon imaginary to txt file.

    Parameters
    ----------
    file_path: str
        Path to out file.
    data: object
        Zipped data arrays. zip(n, k, eps_r, eps_i).

    Returns
    -------
    None

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['n', 'k', 'eps_real', 'eps_imaginary'])
        csv_writer.writerow(data)