import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path


def woollamVASE(file_path : str,
                out_path : str,
                plot_dict : dict) -> dict:
    """
    Process ellipsometry data for a J.A.Woollam spectroscopic ellipsometer.

    Parameters
    ----------
    file_path, out_path: str
        Input file path, output directory path.
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
    out_files: dictionary
        Dictionary containing the file paths for all saved data.

    See Also
    --------

    Notes
    -----

    Example
    -------
    None

    """
    file_name = fp.get_filename(file_path=file_path)
    out_files = {
        "file_name": file_name,
        "fit_file": f'{file_name}.json',
        "nk_path": f'{out_path}/{file_name}_nk.png',
        "eps_path": f'{out_path}/{file_name}_eps.png',
        "data_path": f'{out_path}/{file_name}_Data.txt',
        "model_path": f'{out_path}/{file_name}_Model.png'}
    wavelength, s_psi, s_del, m_psi, m_del = io.ellipsometer_in(
        file_path=file_path)
    fit_file = Path(f'{out_path}/{out_files["fit_file"]}')
    if fit_file.is_file():
        fit = io.load_json(file_path=fit_file)
        if fit["Model"] == "Cauchy":
            n, k = anal.cauchy_fits(
                wavelength=wavelength,
                model=fit)
            eps_real, eps_imag = anal.epsilon(
                refractive_index=n,
                extinction_coefficient=k)
        elif fit["Model"] == "Graded":
            eps_real, eps_imag = anal.graded_material(
                wavelength=wavelength,
                model=fit)
            n, k = anal.comp_RI(
                epsilon_real=eps_real,
                epsilon_imaginary=eps_imag)
        elif fit["Model"] == "Parameterised":
            eps_real, eps_imag = anal.parameterised_materials(
                wavelength=wavelength,
                model=fit)
            n, k = anal.comp_RI(
                epsilon_real=eps_real,
                epsilon_imaginary=eps_imag)
        else:
            n = []
            k = []
            eps_real = []
            eps_imag = []
        arrays = zip(n, k, eps_real, eps_imag)
        if not list(arrays):
            out_files["nk_path"] = "Model Not Implemented"
            out_files["eps_path"] = "Model Not Implemented"
            out_files["data_path"] = "Model Not Implemented"
        else:
            io.ellips_save(
                file_path=Path(f'{out_files["data_path"]}'),
                data=arrays)
            plot.twin_x_plot(
                x=wavelength,
                y1=n,
                y2=k,
                y1_label='n',
                y2_label='k',
                x_axis_label='Wavelength [nm]',
                y1_axis_label='Refractive Index [RIU]',
                y2_axis_label='Extinction Coefficient [RIU]',
                title=out_files["file_name"],
                out_path=Path(f'{out_files["nk_path"]}'),
                plot_dict=plot_dict)
            plot.twin_x_plot(
                x=wavelength,
                y1=eps_real,
                y2=eps_imag,
                y1_label=r'$\varepsilon_{r}$',
                y2_label=r'$\varepsilon_{i}$',
                x_axis_label='Wavelength [nm]',
                y1_axis_label='Epsilon Real [au]',
                y2_axis_label='Epsilon Imaginary [au]',
                title=out_files["file_name"],
                out_path=Path(f'{out_files["eps_path"]}'),
                plot_dict=plot_dict)
    else:
        out_files["fit_file"] = "Data Not Processed Correctly"
        out_files["nk_path"] = "Data Not Processed Correctly"
        out_files["eps_path"] = "Data Not Processed Correctly"
        out_files["data_path"] = "Data Not Processed Correctly"
    if Path(f'{out_files["model_path"]}').is_file():
        pass
    else:
        plot.ellips_plot(
            x=wavelength,
            y1=s_psi,
            y2=m_psi,
            y3=s_del,
            y4=m_del,
            x_axis_label='Wavelength [nm]',
            y_axis_label1=r'${\Psi}$',
            y_axis_label2=r'${\Delta}$',
            title=out_files["file_name"],
            out_path=Path(f'{out_files["model_path"]}'),
            plot_dict=plot_dict)
    return out_files


if __name__ == '__main__':
    '''
    Root set up for Notebooks repository as root directory. Remove '..' to run
    from script from input and output paths.
    '''
    root = Path().absolute()
    vase_dict = io.load_json(
        file_path=Path(
            f'{root}/SpectroscopicAnalysis/vase_dictionary.json'))
    graph_paths = {"out_paths": {}}
    for file in vase_dict["data_files"]:
        file_path = Path(f'{vase_dict["data_path"]}/{file}')
        out_files = woollamVASE(
            file_path=file_path,
            out_path=Path(f'{vase_dict["data_path"]}'),
            plot_dict=vase_dict)
        for key, value in out_files.items():
            if key in graph_paths["out_paths"].keys():
                (graph_paths["out_paths"])[key].append(value)
            else:
                graph_paths["out_paths"].update({key: [value]})
    out_dict = dict(
        vase_dict,
        **graph_paths)
    io.save_json_dicts(
        out_path=Path(
            f'{root}/SpectroscopicAnalysis/vase_dictionary.json'),
        dictionary=out_dict)
