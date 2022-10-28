import os


def check_directory_exists(dir_path):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_path: <string> path to directory
    Return:
        dir_path: <string> path to directory
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)
    else:
        pass
    return dir_path


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def sample_parameters(file_name):
    '''
    Pull sample parameters from file name string.
    Args:
        file_name: <string> file name string
    Return:
        sample_parameters: <dict>
            File Name
            Sample Name
            Grating Period
            Polarisation
            Integration Time
    '''
    file_split = file_name.split('_')
    return {
        "File Name": file_name,
        "Sample Name": file_split[0],
        "Grating Period": (file_split[1])[1:],
        "Polarisation": file_split[2],
        "Integration Time": float((file_split[4])[3: ]) / 1000}


def background_parameters(file_name):
    '''
    Pull background parameters from file name string.
    Args:
        file_name: <string> file name string
    Return:
        background_parameters: <dict>
            File Name
            Sample Name
            Grating Period
            Polarisation
            Integration Time
    '''
    file_split = file_name.split('_')
    return {
        "Bg File Name": file_name,
        "Bg Sample Name": file_split[0],
        "Bg Polarisation": file_split[2],
        "Bg Integration Time": float((file_split[4])[3:]) / 1000}


def extractfile(dir_path,
                file_string):
    '''
    Pull file from directory path.
    Args:
        dir_path: <string> path to file
        file_string: <string> string contained within file name
    Returns:
        array: <array> array of selected files
    '''
    directory_list = sorted(os.listdir(dir_path))
    return [file for file in directory_list if file_string in file]


def find_background(background_path,
                    sample_name,
                    polarisation):
    '''
    Find background intensity spectrum for current sample.
    Args:
        background_path: <string> path to background directory
        sample_name: <string> sample name string
        polarisation: <string> polarsiation orientation string
    Returns:
        background_file: <string> path to background file
    '''
    background_file = os.path.join(
        background_path,
        extractfile(
            dir_path=background_path,
            file_string=(
                f'{sample_name}_Background_{polarisation}'))[0])
    return background_file
