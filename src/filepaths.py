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


def get_parent_directory(file_path):
    '''
    Find parent directory name of target file.
    Args:
        file_path: <string> path to file
    Returns:
        parent_directory: <string> parent directory name (not path)
    '''
    dirpath = os.path.dirname(file_path)
    dirpathsplit = dirpath.split('\\')
    parent_directory = dirpathsplit[-1]
    return parent_directory


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def get_integration_time(file_name):
    '''
    Pull integration time from file name string. Returns an integration time of
    1s without file name containing integration time. Can cope with _int100 or
    _100ms integration times in file name string.
    Args:
        file_name: <string> file name string without extensions
    Returns:
        integration_time: <float> integration time in s
    '''
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


def get_polarisation(file_name):
    '''
    Find polarisation from file name string.
    Args:
        file_name: <string> file name string
    Returns:
        polarisation: <string> polarisation string (TE/TM)
    '''
    file_split = file_name.split('_')
    TE_string = [string for string in file_split if 'TE' in string]
    TM_string = [string for string in file_split if 'TM' in string]
    polarisations = np.append(TE_string, TM_string)
    if len(polarisations) == 0:
        polarisation = 0
    else:
        polarisation = polarisations[0]
    return polarisation


def spectrum_sample_information(file_path):
    '''
    Pull sample parameters from file name string for various processes.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
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


def sample_information(file_path):
    '''
    Pull sample parameters based on which type of file is being analysed.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
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
