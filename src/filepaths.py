import os
import numpy as np

from pathlib import Path
from sys import platform
from src.fileIO import load_json
from src.GUI import prompt_for_path


def check_platform():
    '''
    Check operating system.
    Args:
        None
    Returns:
        operating_system: <string> "Windows", "Linux", or "Mac"
    '''
    if platform == 'linux' or platform == 'linux2':
        operating_system = 'Linux'
    elif platform == 'darwin':
        operating_system = 'Mac'
    elif platform == 'win32':
        operating_system = 'Windows'
    return operating_system


def get_directory_paths(root_path):
    '''
    Get target data path and results path from info dictionary file.
    Args:
        root_path: <string> path to root directory
    Returns:
        data_path: <string> path to data directory
        bg_path: <string> path to background directory
        results_path: <string> path to results directory
        info: <dict> information dictionary (info.json)
    '''
    info = load_json(file_path=Path(f'{root_path}/info.json'))
    directory_paths = {}
    for key, value in info.items():
        if 'Path' in key:
            directory_paths.update({key: Path(f'{root_path}/{value}')})
    return info, directory_paths


def extractfile(directory_path,
                file_string):
    '''
    Pull file from directory path.
    Args:
        directory_path: <string> path to file
        file_string: <string> string contained within file name
    Returns:
        array: <array> array of selected files
    '''
    directory_list = sorted(os.listdir(directory_path))
    return [file for file in directory_list if file_string in file]


def get_files_paths(directory_path,
                    file_string):
    '''
    Get target files and directory paths depending on the operating system.
    Args:
        directory_path: <string> path to data directory
        file_string: <string> file extension (e.g. .csv)
    Returns:
        file_paths: <string> path to files
    '''
    operating_system = check_platform()
    if operating_system == 'Linux' or operating_system == 'Mac':
        file_list = extractfile(
            directory_path=directory_path,
            file_string=file_string)
        file_paths = [Path(f'{directory_path}/{file}') for file in file_list]
    elif operating_system == 'Windows':
        file_paths = prompt_for_path(
            default=directory_path,
            title='Select Target File(s)',
            file_path=True,
            file_type=[(f'{file_string}', f'*{file_string}')])
    return file_paths


def get_parent_directory(file_path : str) -> str:
    """
    Function Details
    ================
    Find parent directory name of target file.

    Parameters
    ----------
    file_path: string
        Path to file.

    Returns
    -------
    parent_directory: string
        Parent directory name (not path).

    See Also
    --------
    os.path.dirname

    Notes
    -----
    None.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Updated documentation.

    """
    dirpath = os.path.dirname(file_path)
    dirpathsplit = dirpath.split('\\')
    parent_directory = dirpathsplit[-1]
    return parent_directory


def get_filename(file_path : str) -> str:
    """
    Function Details
    ================
    Get the file name of a file without the directory path or file extension.

    Split file path and remove directory path and file extensions.

    Parameters
    ----------
    file_path: string
        Path to file.
    
    Returns
    -------
    file_name: string
        File name without path or extension.
    
    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    >>> file_path = "/Path/To/File/File1.txt"
    >>> file_name = get_filename(file_path=file_path)
    >>> file_name
    "File1"

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation update.

    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_integration_time(file_name : str) -> float:
    """
    Function Details
    ================
    Pull integration time from file name string.

    Return integration time if present in the filename.

    Parameters
    ----------
    file_name: string
        File name without extension.

    Returns
    -------
    integration_time: float
        Integration time as a float.

    See Also
    --------
    None.

    Notes
    -----
    If no integration time present in the filename, function will return 1 s. It
    can accept wither an "_int100" or "_100ms" integration time within the file
    name.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Update documentation.

    """
    file_split = file_name.split('_')
    int_time_string = [string for string in file_split if 'int' in string]
    ms_time_string = [string for string in file_split if 'ms' in string]
    time_string = np.append(int_time_string, ms_time_string)
    if len(time_string) == 0:
        integration_time = 1000.00
    else:
        integration_time = (float([
            time[3:] if 'int' in time
            else time[: -2]
            for time in time_string][0])) / 1000
    return integration_time


def get_polarisation(file_name : str) -> str:
    """
    Function Details
    ================
    Find polarisation from file name string.

    Parameters
    ----------
    file_name: string
        File name without extension.

    Returns
    -------
    polarisation: string
        Polarisation = 'TE' or 'TM'.

    See Also
    --------
    None.

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation update.

    """
    file_split = file_name.split('_')
    TE_string = [string for string in file_split if 'TE' in string]
    TM_string = [string for string in file_split if 'TM' in string]
    polarisations = np.append(TE_string, TM_string)
    if len(polarisations) == 0:
        polarisation = 0
    else:
        polarisation = polarisations[0]
    return polarisation


def spectrum_sample_information(file_path : str) -> dict:
    """
    Function Details
    ================
    Pull sample parameters from file name string for various processes.

    Parameters
    ----------
    file_path: string
        Path to file.

    Returns
    -------
    sample_parameters: dict
    >>> {
            'Parent Directory': 'Spectrum/Background',
            'File Name': 'file name',
            'File Path': '/path/to/file',
            'Primary String': 'First Split',
            'Secondary String': 'Second Split',
            'Integration time': 'Integration Time',
            'Polarisation': 'Polarisation String'
        }

    See Also
    --------
    get_parent_directory
    get_filename
    get_polarisation
    get_integration_time

    Notes
    -----
    Parent directory must be named "Spectrum" or "Background" for this function
    to work. This is to distinguish between other software. File names must
    be separated by "_". File names should contain the integration time and the
    polarisation of the incident light either as "int80" or "80ms" for an 80ms
    integration time, or "pol90" or "TE" for a TE polarisation, for example. The
    parent directory is given as a string in the dictionary keys, as detailed in
    the example below.

    Example
    -------
    >>> file_path = '/path/to/Spectrum/A1_Grating_TE_80ms.txt'
    >>> sample_parameters = sample_information(file_path=file_path)
    >>> print(sample_parameters)
    {
        'Parent Directory': 'Spectrum',
        'Spectrum File Name': 'A1_Grating_TE_80ms',
        'Spectrum File Path': '/path/to/Spectrum/A1_Grating_TE_80ms.txt',
        'Spectrum Primary String': 'A1',
        'Spectrum Secondary String': 'Grating_TE',
        'Spectrum Integration Time': 0.08,
        'Spectrum Polarisation': 'TE'
    }

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation updated.

    """
    parent_directory = get_parent_directory(file_path=file_path)
    file_name = get_filename(file_path=file_path)
    file_split = file_name.split('_')
    polarise = get_polarisation(file_name=file_name)
    integration = get_integration_time(file_name=file_name)
    return {
        "Parent Directory": parent_directory,
        f'{parent_directory} File Name': file_name,
        f'{parent_directory} File Path': f'{file_path}',
        f'{parent_directory} Primary String': file_split[0],
        f'{parent_directory} Secondary String': f'{file_split[1]}_{polarise}',
        f'{parent_directory} Integration Time': integration,
        f'{parent_directory} Polarisation': polarise}


def sample_information(file_path : str) -> dict:
    """
    Function Details
    ================
    Pull sample information and parameters based on the type of file being
    processed/analysed.

    Parameters
    ----------
    file_path: string
        Path to target file.

    Returns
    -------
    sample_parameters: dict
        If parent directory is named spectrum/background:
    >>> {
            'Parent Directory': 'Spectrum/Background',
            'File Name': 'file name',
            'File Path': '/path/to/file',
            'Primary String': 'First Split',
            'Secondary String': 'Second Split',
            'Integration time': 'Integration Time',
            'Polarisation': 'Polarisation String'
        }
        If parent directory is not named spectrum/background:
    >>> {}

    See Also
    --------
    spectrum_sample_information
    get_parent_directory

    Notes
    -----
    Parent directory must be named "Spectrum" or "Background" for this function
    to work. This is to distinguish between other software. File names must
    be separated by "_". File names should contain the integration time and the
    polarisation of the incident light either as "int80" or "80ms" for an 80ms
    integration time, or "pol90" or "TE" for a TE polarisation, for example. The
    parent directory is given as a string in the dictionary keys, as detailed in
    the example below.

    Example
    -------
    >>> file_path = '/path/to/Spectrum/A1_Grating_TE_80ms.txt'
    >>> sample_parameters = sample_information(file_path=file_path)
    >>> print(sample_parameters)
    {
        'Parent Directory': 'Spectrum',
        'Spectrum File Name': 'A1_Grating_TE_80ms',
        'Spectrum File Path': '/path/to/Spectrum/A1_Grating_TE_80ms.txt',
        'Spectrum Primary String': 'A1',
        'Spectrum Secondary String': 'Grating_TE',
        'Spectrum Integration Time': 0.08,
        'Spectrum Polarisation': 'TE'
    }

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Update to documentation.

    """
    parent_directory = get_parent_directory(file_path=file_path)
    if parent_directory == 'Spectrum' or parent_directory == 'Background':
        sample_parameters = spectrum_sample_information(
            file_path=file_path)
    else:
        sample_parameters = {}
    return sample_parameters


def get_all_batches(file_paths):
    '''
    Find all sample batches in series of file paths and append file paths to
    batch names for loop processing.
    Args:
        file_paths: <array> array of target file paths
    Returns:
        parent: <string> parent directory string
        batches: <dict>
            Batch inidicators: respective file paths for all samples in batch
    '''
    batches = {}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        print(sample_parameters)
        parent = sample_parameters['Parent Directory']
        key = f'{parent} Primary String'
        if sample_parameters[key] in batches.keys():
            batches[f'{sample_parameters[key]}'].append(file)
        else:
            batches.update({f'{sample_parameters[key]}': [file]})
    return parent, batches


def find_background(background_path,
                    sample_details,
                    file_string):
    '''
    Find background intensity spectrum for current sample.
    Args:
        background_path: <string> path to background directory
        sample_details: <dict> dictionary containing all sample information
        file_string: <string> file path extension
    Returns:
        background_file: <array> path to background file or empty if no file
        bg_details: <dict> background parameters (same as sample_information)
    '''
    parent = sample_details['Parent Directory']
    primary = f'{parent} Primary String'
    polarise = f'{parent} Polarisation'
    try:
        background_files = extractfile(
            directory_path=background_path,
            file_string=file_string)
        background_file = []
        bg_details = {}
        for file in background_files:
            file_path = Path(f'{background_path}/{file}')
            bg_info = sample_information(file_path=file_path)
            bg_parent = bg_info['Parent Directory']
            bg_primary = f'{bg_parent} Primary String'
            bg_polarise = f'{bg_parent} Polarisation'
            if bg_info[bg_primary] == sample_details[primary]:
                if bg_info[bg_polarise] == sample_details[polarise]:
                    background_file.append(file_path)
                    bg_details.update(bg_info)
    except:
        background_file = []
        bg_details = {"BG String": "No BG File"}
    return background_file, bg_details


def update_batch_dictionary(parent,
                            batch_name,
                            file_paths):
    '''
    Update batch results dictionary.
    Args:
        parent: <string> parent directory identifier
        batch_name: <string> batch name identifier
        file_paths: <array> list of target file paths
    Returns:
        batch_dictionary: <dict>
            Batch Name
            File Names
            File Paths
            Secondary Strings
    '''
    batch_dictionary = {
        f'{parent} Batch Name': batch_name,
        f'{parent} File Name': [],
        f'{parent} File Path': [],
        f'{parent} Secondary String': []}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        for key, value in sample_parameters.items():
            if key in batch_dictionary.keys():
                batch_dictionary[key].append(value)
    return batch_dictionary
