import json
import numpy as np


def read_GMRX_file(file_path):
    '''
    Load txt output from GMRX spectrometer. Return wavelength in nm.
    Args:
        file_path: <string> path to file
    Returns:
        wavelength: <array> wavelength array
        intensity: <array> intensity array
    '''
    wavelength, intensity = np.genfromtxt(
        fname=file_path,
        delimiter=';',
        unpack=True)
    return wavelength, intensity


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path,
                    dictionary):
    '''
    Save dictionary to json file.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to save out
    Returns:
        None
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')


def load_json(file_path):
    '''
    Extract user variables from json dictionary.
    Args:
        file_path: <string> path to file
    Returns:
        dictionary: <dict> use variables dictionary
    '''
    with open(file_path, 'r') as file:
        return json.load(file)
