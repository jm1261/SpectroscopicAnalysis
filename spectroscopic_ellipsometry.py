import src.fileIO as io
import src.filepaths as fp
import src.plotting as plot
import src.analysis as anal

from pathlib import Path


def woollamVASE(file_path : str,
                out_path : str,
                plot_dict : dict) -> str:
    """
    """
    file_name = fp.get_filename(file_path=file_path)
    wavelength, s_psi, s_del, m_psi, m_del = io.ellipsometer_in(
        file_path=file_path)
    fit_name = f'{file_name}.json'
    fit_file = Path(f'{out_path}/{fit_name}')
    if fit_file.is_file():
        fit = io.load_json(file_path=fit_file)
        nk_out_path = Path(f'{out_path}/{file_name}_nk.png')
        if nk_out_path.is_file():
            pass
        else:
            n = [
                    anal.cauchy_equation(
                        A=fit["A"][0],
                        B=fit["B"][0],
                        C=fit["C"][0],
                        x=x*1E-3)
                    for x in wavelength]
            plot.xy_plot(
                x=wavelength,
                y=n,
                y_label='n',
                x_axis_label='Wavelength [nm]',
                y_axis_label='Refractive Index [RIU]',
                title=file_name,
                out_path=nk_out_path,
                plot_dict=plot_dict)
    else:
        nk_out_path = 'NULL'
    model_out_path = Path(f'{out_path}/{file_name}_Model.png')
    if model_out_path.is_file():
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
            title=file_name,
            out_path=model_out_path,
            plot_dict=plot_dict)
    return nk_out_path, model_out_path


if __name__ == '__main__':
    '''
    Root setup for Notebooks repository as root directory. Remove '..' to run
    from script.
    '''
    root = Path().absolute()
    vase_dict = io.load_json(
        file_path=Path(
            f'{root}/../SpectroscopicAnalysis/vase_dictionary.json'))
    files = vase_dict["data_files"]
    data_path = vase_dict["data_path"]
    graph_paths = {"out_paths": []}
    for file in files:
        file_path = Path(f'{data_path}/{file}')
        nk_out, model_out = woollamVASE(
            file_path=file_path,
            out_path=data_path,
            plot_dict=vase_dict)
        graph_paths["out_paths"].append(f'{nk_out}')
        graph_paths["out_paths"].append(f'{model_out}')
    out_dict = dict(
        vase_dict,
        **graph_paths)
    io.save_json_dicts(
        out_path=Path(
            f'{root}/../SpectroscopicAnalysis/vase_dictionary.json'),
        dictionary=out_dict)
