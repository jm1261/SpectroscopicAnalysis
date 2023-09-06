import src.fileIO as io
import src.chris as chris
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path


def batch_calculate_peak_wavelength(parent_directory,
                                    batch_name,
                                    file_paths,
                                    directory_paths,
                                    plot_files):
    '''
    Calculate sample batch peak wavelength and error, from individual files
    within batch.
    Args:
        parent_directory: <string> parent directory identifier
        batch_name: <string> batch name string
        file_paths: <array> array of target file paths
        directory_paths: <dict> dictionary containing required paths
        plot_files: <string> "True" or "False" for plotting output
    Returns:
        results_dictionary: <dict>
            Batch Name
            File Names
            File Paths
            Secondary Strings
            Individual file values for:
                Background Files
                Region Trim Index: <array> min, max indices
                popt: <array> fano fit parameters:
                    peak, gamma, q, amplitude, damping
                pcov: <array> fano fit errors
                    peak, gamma, q, amplitude, damping
    '''
    batch_dictionary = fp.update_batch_dictionary(
        parent=parent_directory,
        batch_name=batch_name,
        file_paths=file_paths)
    for file in file_paths:
        wavelength, raw_intensity = io.read_GMR_file(file_path=file)
        sample_parameters = fp.sample_information(file_path=file)
        background_file, background_parameters = fp.find_background(
            background_path=directory_paths['Background Path'],
            sample_details=sample_parameters,
            file_string='.txt')
        print(background_file)
        if len(background_file) == 0:
            normalised_intensity = anal.normalise_intensity(
                raw_intensity=anal.timecorrected_intensity(
                    raw_intensity=raw_intensity,
                    integration_time=sample_parameters[
                        f'{parent_directory} Integration Time']))
        else:
            _, background_raw_intensity = io.read_GMR_file(
                file_path=background_file[0])
            background_parent = background_parameters['Parent Directory']
            normalised_intensity = anal.bg_normal_intensity(
                intensity=raw_intensity,
                background_intensity=background_raw_intensity,
                integration_time=sample_parameters[
                    f'{parent_directory} Integration Time'],
                background_integration_time=background_parameters[
                    f'{background_parent} Integration Time'])
        out_string = sample_parameters[f'{parent_directory} Secondary String']
        plot.spectrumplt(
            wavelength=wavelength,
            intensity=normalised_intensity,
            out_path=Path(f'{directory_paths["Results Path"]}/{batch_name}_{out_string}'))
        peak_results = chris.calc_peakwavelength(
            wavelength=wavelength,
            normalised_intensity=normalised_intensity,
            sample_details=sample_parameters,
            plot_figure=plot_files,
            out_path=Path(
                f'{directory_paths["Results Path"]}'
                f'/{batch_name}_{out_string}_Peak.png'))
        batch_dictionary.update(
            {f'{out_string} File': sample_parameters})
        batch_dictionary.update(
            {f'{out_string} Background': background_parameters})
        batch_dictionary.update(peak_results)
    return batch_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['Spectrum Path'],
        file_string='.txt')
    parent, batches = fp.get_all_batches(file_paths=file_paths)

    ''' Batch Processing '''
    for batch, filepaths in batches.items():
        out_file = Path(
            f'{directory_paths["Results Path"]}'
            f'/{batch}_Peak.json')
        if out_file.is_file():
            pass
        else:
            results_dictionary = batch_calculate_peak_wavelength(
                parent_directory=parent,
                batch_name=batch,
                file_paths=filepaths,
                directory_paths=directory_paths,
                plot_files=info['Plot Files'])
            io.save_json_dicts(
                out_path=out_file,
                dictionary=results_dictionary)
