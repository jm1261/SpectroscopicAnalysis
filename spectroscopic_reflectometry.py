import src.fileIO as io
import src.filepaths as fp
import src.plotting as plot

from pathlib import Path

def spectroscopic_reflectometer(file_path,
                                out_path,
                                plot_dict):
    """
    Plot the n, k and epsilon real, imaginary for Filmetrics spectroscopic
    reflectometer.

    Read .fitnk file and plot data as a function of wavelength, calculate the
    real and imaginary epsilon and plot as a function of wavelength.

    Parameters
    ----------
    file_path, out_path: string
        Path to input file, path to output directory.
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
    
    Returns
    -------
    nk_out_path, eps_out_path: string
        Path to output graphs.
    
    See Also
    --------
    reflectometer_in
    get_filename
    reflectometer_plots

    Notes
    -----
    None

    Example
    -------
    None

    """
    file_name = fp.get_filename(file_path=file_path)
    wavelength, n, k = io.reflectometer_in(file_path=file_path)
    nk_out_path = Path(f'{out_path}/{file_name}_nk.png')
    eps_out_path = Path(f'{out_path}/{file_name}_epsilon.png')
    if nk_out_path.is_file():
        pass
    else:
        plot.reflectometer_plots(
            x=wavelength,
            y1=n,
            y2=k,
            x_axis_label='Wavelength [nm]',
            y_axis_label='Index [au]',
            y1_label='n',
            y2_label='k',
            title=file_name,
            out_path=nk_out_path,
            plot_dict=plot_dict)
    if eps_out_path.is_file():
        pass
    else:
        eps_r = [(a ** 2) - (b ** 2) for a, b in zip(n, k)]
        eps_i = [2 * a * b for a, b, in zip(n, k)]
        plot.reflectometer_plots(
            x=wavelength,
            y1=eps_r,
            y2=eps_i,
            x_axis_label='Wavelength [nm]',
            y_axis_label='Permittivity [au]',
            y1_label=r'$\bf{\epsilon_{r}}$',
            y2_label=r'$\bf{\epsilon_{i}}$',
            title=file_name,
            out_path=eps_out_path,
            plot_dict=plot_dict)
    return nk_out_path, eps_out_path


if __name__ == '__main__':
    '''
    Root setup for Notebooks repository as root directory. Remove '..' to run
    from script.
    '''
    root = Path().absolute()
    filmetrics_dict = io.load_json(
        file_path=Path(
            f'{root}/../SpectroscopicAnalysis/filmetrics_dictionary.json'))
    files = filmetrics_dict["data_files"]
    data_path = filmetrics_dict["data_path"]
    graph_paths = {"out_paths" : []}
    for file in files:
        file_path = Path(f'{data_path}/{file}')
        nk_out, eps_out = spectroscopic_reflectometer(
            file_path=file_path,
            out_path=data_path,
            plot_dict=filmetrics_dict)
        graph_paths["out_paths"].append(f'{nk_out}')
        graph_paths["out_paths"].append(f'{eps_out}')
    out_dict = dict(
        filmetrics_dict,
        **graph_paths)
    io.save_json_dicts(
        out_path=Path(
            f'{root}/../SpectroscopicAnalysis/filmetrics_dictionary.json'),
        dictionary=out_dict)
