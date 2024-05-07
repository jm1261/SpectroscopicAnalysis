import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path


def calc_fanowavelength(file_path : str,
                        out_path : str,
                        plot_dict : dict,
                        background_path=False) -> tuple:
    """
    Function Details
    ================
    Calculate the peak wavelength of a fano resonant structure.

    Parameters
    ----------
    file_path, out_path, background_path: string
        Path to file, path to save, path to background scan (if exists).
    plot_dict: dictionary
        Plot settings dictionary, containing:
            {
                "width": plot width,\n
                "height": plot height,\n
                "dpi": dots per square inch,\n
                "grid": True/False,\n
                "legend_loc": legend location,\n
                "legend_col": legend column number,\n
                "legend_size": size of legend text,\n
                "axis_fontsize": font size for axis labels,\n
                "label_size": size for tick labels
            }

    Return
    ------
    spectrum_path, peak_path: string
        Path to spectrum figure and fano resonance figure.
    peak_results: dict
        Peak results containing the fano function parameters.
    >>> peak_results
    {
        "Parent Directory": parent,
        "Spectrum File Name": file_name,
        "Spectrum File Path": file_path,
        "Spectrum Primary String": primary,
        "Spectrum Secondary String": secondary,
        "Spectrum Integration Time": integration_time,
        "Spectrum Polarisation": polarisation,
        "Spectrum Trim Index": [min, max],
        "Spectrum Fano Fit": [x0, gamma, q, amplitude, damping],
        "Spectrum Fano Errors": [error, error, error, error, error],
        "Spectrum Peak Wavelength": peak,
        "Spectrum Peak Error": error
    }

    See Also
    --------
    read_GMR_file
    sample_information
    bg_normal_intensity
    normalise_intensity
    timecorrected_intensity
    xy_plot
    calculate_fano_peak

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
    Documentation updated. Functions updated to remove the constant passing of
    the sample/file name identifier string.

    """

    ''' Load Target File '''
    wavelength, raw_intensity = io.read_GMR_file(file_path=file_path)
    sample_parameters = fp.sample_information(file_path=file_path)
    

    ''' Load Background File (if Exists) '''
    if background_path:
        background_wavelength, background_intensity = io.read_GMR_file(
            file_path=background_path)
        background_parameters = fp.sample_information(file_path=background_path)

        ''' Normalise to Background '''
        normalised_intensity = anal.bg_normal_intensity(
            intensity=raw_intensity,
            background_intensity=background_intensity,
            integration_time=sample_parameters["Spectrum Integration Time"],
            background_integration_time=background_parameters[
                "Background Integration Time"])

    else:
        ''' Normalise to Integration Time (No Background) '''
        normalised_intensity = anal.normalise_intensity(
            raw_intensity=anal.timecorrected_intensity(
                raw_intensity=raw_intensity,
                integration_time=sample_parameters[
                    'Spectrum Integration Time']))

    ''' Plot Spectrum '''
    spectrum_path = Path(
        f'{out_path}/{sample_parameters["Spectrum File Name"]}.png')
    plot.xy_plot(
        x=wavelength,
        y=normalised_intensity,
        plot_dict=plot_dict,
        x_axis_label='Wavelength [nm]',
        y_axis_label='Normalised Intensity [au]',
        title=sample_parameters["Spectrum File Name"],
        out_path=spectrum_path)

    ''' Calculate Peak Results '''
    peak_path = Path(
            f'{out_path}/{sample_parameters["Spectrum File Name"]}_Peak.png')
    peak_results = anal.calculate_fano_peak(
        wavelength=wavelength,
        normalised_intensity=normalised_intensity,
        sample_details=sample_parameters,
        out_path=peak_path,
        plot_dict=plot_dict)

    ''' Results '''
    results = dict(
        sample_parameters,
        **peak_results)

    return spectrum_path, peak_path, results


if __name__ == '__main__':
    '''
    Due to interactive plotting, this script must be run directly. The plot
    dictionary should be set up prior to running this code.
    '''
    root = Path().absolute()
    peak_dict = io.load_json(
        file_path=Path(f'{root}/SpectroscopicAnalysis/peak_dictionary.json'))
    files = peak_dict["data_files"]
    data_path = peak_dict["data_path"]
    graph_paths = {"out_paths": []}
    background_path = peak_dict["background_path"]
    background_file = peak_dict["background_file"]
    for file in files:
        file_path = Path(f'{data_path}/{file}')
        file_name = fp.get_filename(file_path=file_path)
        if Path(f'{data_path}/{file_name}_Results.json').is_file():
            pass
        else:
            spectrum, peak, results = calc_fanowavelength(
                file_path=file_path,
                out_path=data_path,
                plot_dict=peak_dict,
                background_path=Path(f'{background_path}/{background_file}'))
            graph_paths["out_paths"].append(spectrum)
            graph_paths["out_paths"].append(peak)
            io.save_json_dicts(
                out_path=Path(f'{data_path}/{file_name}_Results.json'),
                dictionary=results)
    out_dict = dict(
        peak_dict,
        **graph_paths)
    io.save_json_dicts(
        out_path=Path(f'{root}/SpectroscopicAnalysis/peak_dictionary.json'),
        dictionary=out_dict)
